const std = @import("std");
const posix = std.posix;
const net = std.net;

pub fn main() !void {
    const port: u16 = 2910; // Przykładowy port serwera
    const addr = try net.Address.parseIp("127.0.0.1", port);
    
    const sock = try posix.socket(posix.AF.INET, posix.SOCK.DGRAM, 0);
    defer posix.close(sock);

    try posix.bind(sock, &addr.any, addr.getOsSockLen());
    std.debug.print("Serwer weryfikujący UDP działa na port {d}...\n", .{port});

    var buf: [1024]u8 = undefined;
    var client_addr: posix.sockaddr = undefined;
    var client_addr_len: posix.socklen_t = @sizeOf(posix.sockaddr);

    while (true) {
        const n = try posix.recvfrom(sock, &buf, 0, &client_addr, &client_addr_len);
        const msg = std.mem.trim(u8, buf[0..n], " \n\r\t");

        // Oczekiwany format: zad14odp;src;60788;dst;2901;data;28
        var response: []const u8 = undefined;

        if (!std.mem.startsWith(u8, msg, "zad14odp;")) {
            response = "BAD_SYNTAX";
        } else {
            // Sprawdzenie poprawności merytorycznej
            const correct_msg = "zad14odp;src;60788;dst;2901;data;28";
            
            if (std.mem.eql(u8, msg, correct_msg)) {
                response = "TAK";
            } else {
                // Jeśli format jest OK (zaczyna się od zad14odp;), ale wartości są złe
                // Sprawdzamy czy ma odpowiednią liczbę średników (uproszczony walidator formatu)
                const semicolon_count = std.mem.count(u8, msg, ";");
                if (semicolon_count == 6) {
                    response = "NIE";
                } else {
                    response = "BAD_SYNTAX";
                }
            }
        }

        _ = try posix.sendto(sock, response, 0, &client_addr, client_addr_len);
        std.debug.print("Otrzymano: {s} -> Odpowiedź: {s}\n", .{ msg, response });
    }
}
