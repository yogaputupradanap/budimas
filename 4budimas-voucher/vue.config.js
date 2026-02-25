const { defineConfig } = require("@vue/cli-service");
const path = require("path");
const rootPath = path.resolve(__dirname, "./");
const webpack = require('webpack')

module.exports = defineConfig({
  // TAMBAHKAN BARIS INI
  // Menggunakan './' agar aset dipanggil secara relatif terhadap lokasi index.html
  publicPath: process.env.NODE_ENV === 'production' ? './' : '/',

  transpileDependencies: true,
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: "false",
      }),
    ],
  },
  chainWebpack: (config) => {
    config.resolve.alias.set("@", rootPath);
  },
});