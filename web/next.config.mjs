const upstream = process.env.CALLPATH_UPSTREAM || "http://api:8000";

export default {
  output: "standalone",
  poweredByHeader: false,
  async rewrites() {
    return [{ source: "/api/:path*", destination: `${upstream}/:path*` }];
  },
};
