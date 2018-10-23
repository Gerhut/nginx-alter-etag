const Koa = require('koa')
const conditionalGet = require('koa-conditional-get')
const etag = require('koa-etag')

const app = exports = module.exports = new Koa()

app.use(conditionalGet())
app.use(etag())

app.use(async context => {
  console.log('If-None-Match', context.get('If-None-Match'))
  context.body = `Content of ${context.url} with etag.`
})

if (require.main === module) {
  app.listen(process.env.PORT)
}
