use std::io::{stdin, stdout, StdinLock, BufReader, BufWriter, BufRead, Write};

#[allow(unused_must_use)]
fn main() {
    let (std_in, std_out) = (stdin(), stdout());
    let br = &mut BufReader::new(std_in.lock());
    let bw = &mut BufWriter::new(std_out.lock());
    
}



// Functions for reading inputs ///////////////////////////////////////

#[allow(dead_code)]
fn rs(br: &mut BufReader<StdinLock>) -> Vec<char> {
    let mut buf = String::new();
    br.read_line(&mut buf).ok();
    buf.trim().chars().collect()
}

#[allow(dead_code)]
fn rn<T: std::str::FromStr>(br: &mut BufReader<StdinLock>) -> T {
    let mut buf = String::new();
    br.read_line(&mut buf).ok();
    buf.trim().parse().ok().unwrap()
}

#[allow(dead_code)]
fn rvs(br: &mut BufReader<StdinLock>) -> Vec<Vec<char>> {
    let mut buf = String::new();
    br.read_line(&mut buf).ok();
    buf.trim().split_whitespace().map(|e| e.chars().collect()).collect()
}

#[allow(dead_code)]
fn rvn<T: std::str::FromStr>(br: &mut BufReader<StdinLock>) -> Vec<T> {
    let mut buf = String::new();
    br.read_line(&mut buf).ok();
    buf.trim().split_whitespace().map(|e| e.parse().ok().unwrap()).collect()
}