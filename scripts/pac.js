function FindProxyForURL(url, host) {
  if (url.substring(0,5) == 'http:' && 
      !isPlainHostName(host) && 
      !shExpMatch(host, '*.local') && 
      !isInNet(dnsResolve(host), '10.0.0.0', '255.0.0.0') && 
      !isInNet(dnsResolve(host), '172.16.0.0',  '255.240.0.0') && 
      !isInNet(dnsResolve(host), '192.168.0.0',  '255.255.0.0') && 
      !isInNet(dnsResolve(host), '127.0.0.0', '255.255.255.0') && 
    return 'HTTPS proxy.googlezip.net:443; PROXY compress.googlezip.net:80; PROXY 74.125.205.211:80; DIRECT';
  return 'DIRECT';
}
