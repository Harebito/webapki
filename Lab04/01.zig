const std = @import("std");

pub fn main() !void {
    const port = 8081;
    const address = try std.net.Address.parseIp4("127.0.0.1", port);
    
    var server = try address.listen(.{ .reuse_address = true });
    defer server.deinit();

    std.debug.print("1. Serwer TCP (Czas) nasłuchuje na 127.0.0.1:{d}...\n", .{port});

    while (true) {
        const connection = try server.accept();
        defer connection.stream.close();

        var buffer: [1024]u8 = undefined;
        // Odbiera wiadomość od klienta
        _ = try connection.stream.read(&buffer);

        const timestamp = std.time.timestamp();
        var out_buf: [128]u8 = undefined;
        const time_str = try std.fmt.bufPrint(&out_buf, "Aktualny czas (UNIX): {d}\n", .{timestamp});
        
        // Odsyła odpowiedź
        _ = try connection.stream.write(time_str);
    }
}
