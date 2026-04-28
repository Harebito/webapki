const std = @import("std");
const net = std.net;

pub fn main() !void {
    const address = try net.Address.parseIp("127.0.0.1", 8081);
    var server = try address.listen(.{ .reuse_address = true });
    defer server.deinit();

    while (true) {
        const conn = try server.accept();
        defer conn.stream.close();

        var buf: [1024]u8 = undefined;
        const n = try conn.stream.read(&buf);
        try conn.stream.writeAll(buf[0..n]);
    }
}
