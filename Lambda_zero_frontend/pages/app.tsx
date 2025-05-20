import type { AppProps } from "next/app";
import React from "react";

function MyApp({ Component, pageProps }: AppProps) {
  // You can add global providers or styles here
  return <Component {...pageProps} />;
}

export default MyApp;
