use std::{
    io::{ Error, ErrorKind, Read, Write },
    net::{ Ipv4Addr, SocketAddr, SocketAddrV4, TcpListener, TcpStream },
    str::{ self, FromStr },
    thread,
    time::Duration,
};
use rand::random;

use aes_gcm::{ Aes256Gcm, KeyInit, aead::Aead };
use chacha20::{ cipher::{ KeyIvInit, StreamCipher }, ChaCha20 };

static KEY: &[u8; 32] = b"ABCDEFGHIJKLMNOPABCDEFGHIJKLMNOP";
static NONCE: &[u8; 12] = b"QRSTUVWXYZ12";

struct Server {
    sock_addr: SocketAddrV4,
}

struct Zombie {
    sock_addr: SocketAddrV4,
    stream: TcpStream,
    chacha: ChaCha20,
}

impl Zombie {
    pub fn encrypt(&mut self, msg: &[u8]) -> Result<Vec<u8>, &'static str> {
        let mut buffer = vec![0; msg.len()];
        buffer.clone_from_slice(msg);
        self.chacha.apply_keystream(&mut buffer);
        Ok(buffer)
    }

    pub fn register(&mut self) -> bool {
        let mut hello: [u8; 5] = [0u8; 5];
        let Ok(_) = self.stream.read(&mut hello) else {
            return false;
        };
        let Ok(msg) = self.encrypt(&hello) else {
            return false;
        };
        let str_msg = String::from_utf8_lossy(&msg).to_string();
        "HELLO" == str_msg
    }

    fn send_flag(&mut self) -> Result<bool, Box<dyn std::error::Error>> {
        let flag = std::env::var("FLAG").unwrap_or("CYBN{REDACTED}".to_string());

        let rand_key: &mut [u8; 32] = &mut [0u8; 32];
        for i in 0..rand_key.len() {
            rand_key[i] = random();
        }

        let rand_nonce: &mut [u8; 12] = &mut [0u8; 12];
        for i in 0..rand_nonce.len() {
            rand_nonce[i] = random();
        }

        let key = aes_gcm::Key::<Aes256Gcm>::from_slice(rand_key);
        let nonce = aes_gcm::Nonce::from_slice(rand_nonce);
        let aes_cipher = Aes256Gcm::new(&key);

        let flag_cipher = aes_cipher
            .encrypt(nonce, flag.as_bytes())
            .expect("Could not encrypt flag, this is very problematique");

        let plain = format!("{}++++{}", hex::encode(rand_key), hex::encode(rand_nonce));
        let ciphertext = self.encrypt(plain.as_bytes())?;
        self.stream.write(&ciphertext)?;

        let mut res = [0u8; 11];
        self.stream.read(&mut res)?;
        if let Ok(plain) = self.encrypt(&res) {
            let str_plain = String::from_utf8_lossy(&plain).to_string();
            if str_plain == "ESTABLISHED" {
                self.stream.write(hex::encode(&flag_cipher).as_bytes())?;
                self.stream.write(b"\n")?;
                return Ok(true);
            }
        }

        self.stream.write(b"{Nah_u_r_a_c0p}")?;
        self.stream.write(b"\n")?;
        Ok(false)
    }

    pub fn handle_client(&mut self) {
        println!("[+] New kitten showing up from {:?}", self.sock_addr);
        if self.register() {
            println!("[+] Kitten successfully registered.");
            match self.send_flag() {
                Ok(valid) => {
                    if valid {
                        println!(
                            "[*] Head pat and flag sent to {:?} as he is a good kitten ...",
                            self.sock_addr
                        );
                    } else {
                        println!("[-] {:?} don't deserve a pet after all ...", self.sock_addr)
                    }
                }
                Err(e) => println!("[-] {:?} failed : {e:?}", self.sock_addr),
            }
        } else {
            println!("[!] Impostor detected !");
            self.stream.write(b"IMPOSTOR").unwrap_or(0);
        }
    }
}

impl TryFrom<TcpStream> for Zombie {
    type Error = std::io::Error;
    fn try_from(stream: TcpStream) -> Result<Self, std::io::Error> {
        let sock_addr = match stream.peer_addr()? {
            SocketAddr::V4(addr) => addr,
            SocketAddr::V6(_) => {
                return Err(Error::from(ErrorKind::Unsupported));
            }
        };
        stream.set_read_timeout(Some(Duration::from_secs(2)))?;
        stream.set_write_timeout(Some(Duration::from_secs(2)))?;

        let chacha: ChaCha20 = ChaCha20::new(KEY.into(), NONCE.into());
        Ok(Self { sock_addr, stream, chacha })
    }
}

impl Server {
    pub fn new(addr: &str, port: u16) -> Self {
        let ipv4addr: Ipv4Addr = Ipv4Addr::from_str(addr).expect("Invalid IPv4");
        let sock_addr: SocketAddrV4 = SocketAddrV4::new(ipv4addr, port);
        Self { sock_addr }
    }

    pub fn start(self) {
        let listener = TcpListener::bind(self.sock_addr).expect(
            format!("Could not bind server to {:#?}", self.sock_addr).as_ref()
        );
        println!("[*] Bind {:?}", self.sock_addr);
        for mb_stream in listener.incoming() {
            if let Ok(stream) = mb_stream {
                let mb_zombie: Result<Zombie, _> = stream.try_into();
                match mb_zombie {
                    Ok(mut zombie) => {
                        thread::spawn(move || zombie.handle_client());
                    }
                    Err(e) => {
                        println!("[-] Error while while adopting kitten :( : {e:#?}");
                    }
                }
            }
        }
    }
}

fn main() {
    println!("--=-=--=-=--=-=--=-=-=-=-");
    println!("        M3OW_B0T C2      ");
    println!("--=-=--=-=--=-=--=-=-=-=-");

    let srv = Server::new("127.0.0.1", 8080);
    srv.start();
}
