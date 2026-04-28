const std = @import("std");
const posix = std.posix;
const net = std.net;

pub fn main() !void {
    const port: u16 = 2909; 
    const addr = try net.Address.parseIp("127.0.0.1", port);
    
    const sock = try posix.socket(posix.AF.INET, posix.SOCK.DGRAM, 0);
    defer posix.close(sock);

    try posix.bind(sock, &addr.any, addr.getOsSockLen());
    std.debug.print("Serwer weryfikujący TCP (Zad 14) działa na porcie {d}...\n", .{port});

    var buf: [1024]u8 = undefined;
    var client_addr: posix.sockaddr = undefined;
    var client_addr_len: posix.socklen_t = @sizeOf(posix.sockaddr);

    while (true) {
        const n = try posix.recvfrom(sock, &buf, 0, &client_addr, &client_addr_len);
        const msg = std.mem.trim(u8, buf[0..n], " \n\r\t");

        var response: []const u8 = undefined;

        // Oczekiwany format: zad13odp;src;2900;dst;35211;data;8
        if (!std.mem.startsWith(u8, msg, "zad13odp;")) {
            response = "BAD_SYNTAX";
        } else {
            const correct_msg = "zad13odp;src;2900;dst;35211;data;8";
            
            if (std.mem.eql(u8, msg, correct_msg)) {
                response = "TAK";
            } else {
                // Walidacja struktury (liczba średników)
                if (std.mem.count(u8, msg, ";") == 6) {
                    response = "NIE";
                } else {
                    response = "BAD_SYNTAX";
                }
            }
        }

        _ = try posix.sendto(sock, response, 0, &client_addr, client_addr_len);
        std.debug.print("Klient: {s} -> {s}\n", .{ msg, response });
    }
}
