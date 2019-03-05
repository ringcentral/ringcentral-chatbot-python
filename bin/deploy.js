

const {readFileSync, writeFileSync} = require('fs')
const {exec} = require('child_process')
const yaml = require('js-yaml')
const {resolve} = require('path')
const cwd = resolve(__dirname, '../dev/lambda')
const execAsync = (cmd, options = {
  cwd
}) => {
  return new Promise((resolve, reject) => {
    exec(cmd, options, (code, stdout, stderr) => {
      if (stderr) {
        return reject(stderr)
      }
      resolve(stdout)
    })
  })
}

function readYml(path) {
  // Get document, or throw exception on error
  return yaml.safeLoad(
    readFileSync(path, 'utf8')
  )
}
const {log} = console

async function run() {
  log('start deploy')
  let file = resolve(__dirname, '../dev/lambda/serverless.yml')
  let yml = readYml(file)
  console.log(yml, 'yml')
  let url = yml.provider.environment.RINGCENTRAL_BOT_SERVER
  // if (!url || !/^https:\/\/.+\.amazonaws\.com.+/.test(url)) {
  //   console.log('please set correct RINGCENTRAL_CHATBOT_SERVER in dist/.env.yml')
  //   process.exit(1)
  // }
  let cmd2 = '../../node_modules/.bin/sls deploy'
  log(`run cmd: ${cmd2}`)
  let res1 = await execAsync(cmd2).catch(log)
  console.log(res1)
  if (!res1) {
    return log('build fails')
  }
  let reg = /(https:\/\/.+\.amazonaws\.com).+\}/
  let arr = res1.match(reg)
  if (!arr || !arr[1]) {
    return log('build fails')
  }
  let urlReal = `${arr[1]}/dev`
  log(`RINGCENTRAL_CHATBOT_SERVER in api gate way: ${urlReal}`)
  if (urlReal !== url) {
    log('modify RINGCENTRAL_BOT_SERVER in dist/server.yml')
    yml.provider.environment.RINGCENTRAL_BOT_SERVER = urlReal
    let newYml = yaml.safeDump(yml)
    writeFileSync(file, newYml)
    run()
  }
}

run()
