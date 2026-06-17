// Learn more https://docs.expo.io/guides/customizing-metro
const { getDefaultConfig } = require('expo/metro-config');
const { withUniwindConfig } = require('uniwind/metro'); 
const path = require('path');

const projectRoot = __dirname;
const workspaceRoot = path.resolve(projectRoot, '../..');

/** @type {import('expo/metro-config').MetroConfig} */
const config = getDefaultConfig(projectRoot);


config.watchFolders = [
  path.resolve(workspaceRoot, 'packages'),
  path.resolve(workspaceRoot, 'node_modules')
];

config.resolver.unstable_enableSymlinks = true;
config.resolver.unstable_enablePackageExports = true;
config.resolver.nodeModulesPaths = [
  path.resolve(projectRoot, 'node_modules'),
  path.resolve(workspaceRoot, 'node_modules'),
  path.resolve(workspaceRoot, 'node_modules/.pnpm/node_modules')
]

// Pin singletons and expo packages to prevent duplicate instances and ensure resolution
// const singletons = [
//   'react',
//   'react-native',
//   'expo',
//   'expo-router',
//   'expo-modules-core',
//   'expo-constants',
//   '@expo/metro-runtime',
// ];
// config.resolver.extraNodeModules = singletons.reduce((acc, name) => {
//   acc[name] = path.resolve(projectRoot, 'node_modules', name);
//   return acc;
// }, {});

// // Add SVG support
// config.transformer.babelTransformerPath = require.resolve('react-native-svg-transformer');
// config.resolver.assetExts = config.resolver.assetExts.filter(ext => ext !== 'svg');
// config.resolver.sourceExts = [...config.resolver.sourceExts, 'svg'];


module.exports = withUniwindConfig(config, {  
  cssEntryFile: '../../global.css', 
  dtsFile: './uniwind-types.d.ts'
});