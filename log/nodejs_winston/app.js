const tracer = require('dd-trace').init({
     env: "dev",
     service: "hello_node",
     logInjection: true
});

const formats = require('dd-trace/ext/formats');
const express = require('express')
const app = express()
const port = 3000
const { createLogger, format, transports } = require('winston');

const httpTransportOptions = {
  host: 'http-intake.logs.datadoghq.com',
  path: '/v1/input/{YOUR_API_KEY}?ddsource=nodejs&service=hello_node',
  ssl: true,
  json: true
};

const logger = createLogger({
  level: 'info',
  exitOnError: false,
  format: format.json(),
  transports: [
    new transports.Http(httpTransportOptions),
//    new transports.File({ filename: 'winston.log'}),
  ],
});

module.exports = logger;

app.get('/', (req, res) => {
  const span = tracer.scope().active();
  msg = "log message to send";
  const record = { msg };

  if (span) {
      tracer.inject(span.context(), formats.LOG, record);
  }

  //sending logs to console & logger(Datadog)
  console.log(JSON.stringify(record));
  logger.log('info', JSON.stringify(record));

  res.send('Hello World!')
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
