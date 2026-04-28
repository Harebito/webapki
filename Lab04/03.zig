const std = @import("std");
const posix = std.posix;

pub fn main() !void {
    const addr = try std.net.Address.parseIp("127.0.0.1", 8082);
    const sock = try posix.socket(posix.AF.INET, posix.SOCK.DGRAM, 0);
    defer posix.close(sock);

    try posix.bind(sock, &addr.any, addr.getOsSockLen());

    var buf: [1024]u8 = undefined;
    var client_addr: posix.sockaddr = undefined;
    var client_addr_len: posix.socklen_t = @sizeOf(posix.sockaddr);

    while (true) {
        const n = try posix.recvfrom(sock, &buf, 0, &client_addr, &client_addr_len);
        _ = try posix.sendto(sock, buf[0..n], 0, &client_addr, client_addr_len);
    }
}
