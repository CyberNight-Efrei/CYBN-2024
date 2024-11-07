def read_nfc_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        lines = data.split('\n')
        blocks = []
        for l in lines:
            if l.startswith('Block'):
                blocks.append(bytes.fromhex(l.split(': ')[1]))
        return b''.join(blocks)

def bytes_to_num_le(data, length):
    return int.from_bytes(data[:length], 'little')

def checksum(refill_block):
    xor_result = 0
    for byte in refill_block:
        xor_result ^= byte
    return xor_result == 0

def parse_csc_data(nfc_data):
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
        return (f"CSC Service Works\n"
                f"New Card\n"
                f"Card Value: {refilled_balance_dollar}.{refilled_balance_cent:02d} CAD\n"
                f"Card Usages Left: {card_lives}")
    else:
        if not checksum_valid:
            raise ValueError("Checksum failed")
        return (f"CSC Service Works\n"
                f"Balance: {current_balance_dollar}.{current_balance_cent:02d} CAD\n"
                f"Last Top-up: {refilled_balance_dollar}.{refilled_balance_cent:02d} CAD\n"
                f"Top-up Count: {refill_times}\n"
                f"Card Usages Left: {card_lives}")

def update_balance(nfc_data, new_balance):
    # Extract blocks
    current_balance_block = nfc_data[4 * 16:4 * 16 + 4]  # Block 4
    current_balance_block_bis = nfc_data[4 * 16 + 8:(4 + 1) * 16]  # Block 4 part 2
    current_balance_copy_block = nfc_data[8 * 16:8 * 16 + 4]  # Block 8
    current_balance_copy_block_bis = nfc_data[8 * 16 + 8:(8 + 1) * 16]  # Block 8 part 2

    # Verify memory format (checksum is later)
    current_balance_and_times = bytes_to_num_le(current_balance_block[:4], 4)
    current_balance_and_times_bis = bytes_to_num_le(current_balance_block_bis[:4], 4)
    current_balance_and_times_copy = bytes_to_num_le(current_balance_copy_block[:4], 4)
    current_balance_and_times_copy_bis = bytes_to_num_le(current_balance_copy_block_bis[:4], 4)

    # Failed verification if balance != backup
    if current_balance_and_times != current_balance_and_times_copy:
        raise ValueError("Backup verification failed")

    if current_balance_and_times_bis != current_balance_and_times_copy_bis:
        raise ValueError("Backup verification failed")

    # Even if balance = 0, e.g., new card, refilled times can't be zero
    if current_balance_and_times == 0 or current_balance_and_times_copy == 0:
        raise ValueError("Value bytes empty")

    # Parse data
    current_balance_block = new_balance.to_bytes(2, 'little') + current_balance_block[2:]
    current_balance_block_parity = bytes([~byte & 0xFF for byte in current_balance_block])
    current_balance_block_bis = new_balance.to_bytes(2, 'little') + current_balance_block_bis[2:]
    current_balance_copy_block = new_balance.to_bytes(2, 'little') + current_balance_copy_block[2:]
    current_balance_copy_block_parity = bytes([~byte & 0xFF for byte in current_balance_copy_block])
    current_balance_copy_block_bis = new_balance.to_bytes(2, 'little') + current_balance_copy_block_bis[2:]

    return nfc_data[:4 * 16] + current_balance_block + current_balance_block_parity + current_balance_block_bis + nfc_data[5 * 16:8 * 16] + current_balance_copy_block + current_balance_copy_block_parity + current_balance_copy_block_bis + nfc_data[9 * 16:]


def update_refilled(nfc_data, new_refilled):
    # Extract blocks
    refill_block = nfc_data[2 * 16:(2 + 1) * 16]  # Block 2

    # Update data
    refill_block = refill_block[:9] + new_refilled.to_bytes(2, 'little') + refill_block[11:]

    # Step 2: Calculate XOR of all bytes except 16
    xor_sum = 0
    for i, byte in enumerate(refill_block):
        if i != 15:  # Skipping byte 16 (indexing is 0-based)
            xor_sum ^= byte

    # Update checksum
    refill_block = refill_block[:15] + xor_sum.to_bytes(1, 'little')
    # Ensure that the new block has a correct checksum
    xor_sum = 0
    for i, byte in enumerate(refill_block):
        xor_sum ^= byte
    # assert checksum(refill_block), "Checksum is not valid!"

    return nfc_data[:2 * 16] + refill_block + nfc_data[3 * 16:]

def write_nfc_file(file_path, nfc_data):
    with open(file_path, 'w') as file:
        with open('header.txt', 'r') as header:
            file.write(header.read())
        for i in range(64):
            # Write block in format 'Block i: 01 23 45 67 89 AB CD EF 01 23 45 67 89 AB CD EF'
            file.write(f"Block {i}: ")
            for j in range(16):
                file.write(f"{nfc_data[i * 16 + j]:02X} ")
            file.write('\n')

def main():
    nfc_data = read_nfc_file('blank_card.nfc')
    # nfc_data_test = read_nfc_file('3_USD_Test.nfc')
    print(parse_csc_data(nfc_data))
    nfc_data = update_balance(nfc_data, 4000)
    nfc_data = update_refilled(nfc_data, 4000)
    write_nfc_file('filled_card.nfc', nfc_data)

if __name__ == "__main__":
    main()

