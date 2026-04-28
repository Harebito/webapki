const std = @import("std");
const posix = std.posix;

pub fn main() !void {
    const sock = try posix.socket(posix.AF.INET, posix.SOCK.DGRAM, 0);
    const addr = try std.net.Address.parseIp("127.0.0.1", 8083);
    try posix.bind(sock, &addr.any, addr.getOsSockLen());

    var buf: [1024]u8 = undefined;
    var client_addr: posix.sockaddr = undefined;
    var client_addr_len: posix.socklen_t = @sizeOf(posix.sockaddr);

    while (true) {
        const n = try posix.recvfrom(sock, &buf, 0, &client_addr, &client_addr_len);
        const input = std.mem.trim(u8, buf[0..n], " \n\r\t");
        
        var it = std.mem.tokenizeAny(u8, input, " ");
        const a_str = it.next() orelse continue;
        const op = it.next() orelse continue;
        const b_str = it.next() orelse continue;

        const a = std.fmt.parseInt(i32, a_str, 10) catch 0;
        const b = std.fmt.parseInt(i32, b_str, 10) catch 0;

        const result = switch (op[0]) {
            '+' => a + b,
            '-' => a - b,
            '*' => a * b,
            '/' => if (b != 0) @divTrunc(a, b) else 0,
            else => 0,
        };

        var out_buf: [64]u8 = undefined;
        const msg = try std.fmt.bufPrint(&out_buf, "Wynik: {d}\n", .{result});
        _ = try posix.sendto(sock, msg, 0, &client_addr, client_addr_len);
    }
}
