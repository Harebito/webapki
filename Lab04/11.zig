const std = @import("std");
const posix = std.posix;
const net = std.net;

pub fn main() !void {
    const port: u16 = 2911;
    const addr = try net.Address.parseIp("127.0.0.1", port);
    
    const sock = try posix.socket(posix.AF.INET, posix.SOCK.DGRAM, 0);
    defer posix.close(sock);

    try posix.bind(sock, &addr.any, addr.getOsSockLen());
    std.debug.print("Serwer Zad 15 (IP/TCP) działa na porcie {d}...\n", .{port});

    var buf: [1024]u8 = undefined;
    var client_addr: posix.sockaddr = undefined;
    var client_addr_len: posix.socklen_t = @sizeOf(posix.sockaddr);

    while (true) {
        const n = try posix.recvfrom(sock, &buf, 0, &client_addr, &client_addr_len);
        const msg = std.mem.trim(u8, buf[0..n], " \n\r\t");
        var response: []const u8 = "BAD_SYNTAX";

        if (std.mem.startsWith(u8, msg, "zad15odpA;")) {
            const correctA = "zad15odpA;ver;4;srcip;212.182.24.27;dstip;192.168.0.2;type;6";
            if (std.mem.eql(u8, msg, correctA)) {
                response = "TAK";
            } else if (std.mem.count(u8, msg, ";") == 8) {
                response = "NIE";
            }
        } else if (std.mem.startsWith(u8, msg, "zad15odpB;")) {
            const correctB = "zad15odpB;srcport;2900;dstport;47526;data;26";
            if (std.mem.eql(u8, msg, correctB)) {
                response = "TAK";
            } else if (std.mem.count(u8, msg, ";") == 6) {
                response = "NIE";
            }
        }

        _ = try posix.sendto(sock, response, 0, &client_addr, client_addr_len);
    }
}
