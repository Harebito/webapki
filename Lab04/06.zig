const std = @import("std");
const posix = std.posix;

// Zamiast @cImport, deklarujemy funkcję zewnętrzną z C
extern fn lookup_hostname(ip_str: [*:0]const u8, buffer: [*]u8, buffer_len: usize) c_int;

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    const sock = try posix.socket(posix.AF.INET, posix.SOCK.DGRAM, 0);
    defer posix.close(sock);

    const addr = try std.net.Address.parseIp("127.0.0.1", 8085);
    try posix.bind(sock, &addr.any, addr.getOsSockLen());

    var buf: [1024]u8 = undefined;
    var client_addr: posix.sockaddr = undefined;
    var client_addr_len: posix.socklen_t = @sizeOf(posix.sockaddr);

    while (true) {
        const n = try posix.recvfrom(sock, &buf, 0, &client_addr, &client_addr_len);
        const input = std.mem.trim(u8, buf[0..n], " \n\r\t");

        var response_buf: [256]u8 = undefined;
        var final_msg: []const u8 = undefined;

        // Musimy dodać \0 na końcu stringa dla C
        const input_c = try allocator.dupeZ(u8, input);
        defer allocator.free(input_c);

        var hostname_buf: [256]u8 = undefined;
        
        // Wywołanie funkcji z dns_helper.c
        if (lookup_hostname(input_c, &hostname_buf, hostname_buf.len) == 0) {
            const name = std.mem.span(@as([*:0]const u8, @ptrCast(&hostname_buf)));
            final_msg = try std.fmt.bufPrint(&response_buf, "Hostname: {s}", .{name});
        } else {
            // Próba Hostname -> IP
            if (std.net.getAddressList(allocator, input, 0)) |list| {
                defer list.deinit();
                if (list.addrs.len > 0) {
                    final_msg = try std.fmt.bufPrint(&response_buf, "IP: {any}", .{list.addrs[0]});
                } else final_msg = "Brak wyników";
            } else |_| {
                final_msg = "Błąd formatu/DNS";
            }
        }

        _ = try posix.sendto(sock, final_msg, 0, &client_addr, client_addr_len);
    }
}
