from flask import Flask, request, render_template
from base64 import b64decode
from os import environ

app = Flask(__name__)


def bytes_to_num_le(data, length):
    return int.from_bytes(data[:length], 'little')


def checksum(refill_block):
    xor_result = 0
    for byte in refill_block:
        xor_result ^= byte
    return xor_result == 0


def parse_card_data(card_data: str):
    lines = b64decode(card_data).decode('utf-8').split('\n')
    blocks = []
    for l in lines:
        if l.startswith('Block'):
            blocks.append(bytes.fromhex(l.split(': ')[1]))
    nfc_data = b''.join(blocks)
    # Extract blocks
    refill_block = nfc_data[2 * 16:(2 + 1) * 16]  # Block 2
    current_balance_block = nfc_data[4 * 16:(4 + 1) * 16]  # Block 4
    current_balance_copy_block = nfc_data[8 * 16:(8 + 1) * 16]  # Block 8
    card_lives_block = nfc_data[9 * 16:(9 + 1) * 16]  # Block 9
    refill_sign_block = nfc_data[13 * 16:(13 + 1) * 16]  # Block 13

    # Verify memory format (checksum is later)
    current_balance_and_times = bytes_to_num_le(current_balance_block[:4], 4)
    current_balance_and_times_copy = bytes_to_num_le(current_balance_copy_block[:4], 4)

    # Failed verification if balance != backup
    if current_balance_and_times != current_balance_and_times_copy:
        raise ValueError("Backup verification failed")

    # Even if balance = 0, e.g., new card, refilled times can't be zero
    if current_balance_and_times == 0 or current_balance_and_times_copy == 0:
        raise ValueError("Value bytes empty")

    # Parse data
    refilled_balance = bytes_to_num_le(refill_block[9:], 2)
    current_balance = bytes_to_num_le(current_balance_block[:2], 2)
    card_lives = bytes_to_num_le(card_lives_block, 2)
    refill_times = bytes_to_num_le(refill_block[5:7], 2)
    refill_sign = bytes_to_num_le(refill_sign_block, 8)

    # Calculate balances in dollars and cents
    refilled_balance_dollar = refilled_balance // 100
    refilled_balance_cent = refilled_balance % 100
    current_balance_dollar = current_balance // 100
    current_balance_cent = current_balance % 100

    # Last byte of refill block is checksum
    checksum_valid = checksum(refill_block)

    if refill_sign == 0 and refill_times == 1:
        return {"refilled_balance": float(f"{refilled_balance_dollar}.{refilled_balance_cent:02d}")}
    else:
        if not checksum_valid:
            raise ValueError("Checksum failed")
        return {
            "balance": float(f"{current_balance_dollar}.{current_balance_cent:02d}"),
            "refilled_balance": float(f"{refilled_balance_dollar}.{refilled_balance_cent:02d}"),
        }


@app.context_processor
def utility_processor():
    def format_price(amount):
        return f"{amount:.2f}".replace(".", ",")
    def get_flag():
        return environ.get("FLAG", "FLAG{this_is_a_fake_flag}")
    return dict(format_price=format_price, get_flag=get_flag)


def is_showing_flag(card_parsed_data):
    if 'balance' in card_parsed_data and 'refilled_balance' in card_parsed_data and 4.0 <= card_parsed_data['balance'] <= card_parsed_data['refilled_balance']:
        return True
    return False


@app.route('/', methods=['GET', 'POST'])
def home():
    if 'card_data' in request.form:
        try:
            card_data = request.form['card_data']
            card_parsed_data = parse_card_data(card_data)
            return render_template('index.jinja2', card_data=card_parsed_data, show_flag=is_showing_flag(card_parsed_data))
        except ValueError as e:
            return render_template('index.jinja2', card_data=None, error=str(e), show_flag=False)
        except Exception as e:
            print(e)
            return render_template('index.jinja2', card_data=None, error="La carte fournie n'est pas valide", show_flag=False)
    return render_template('index.jinja2', card_data=None, show_flag=False)


if __name__ == '__main__':
    app.run(host='', port=6000, debug=False)
