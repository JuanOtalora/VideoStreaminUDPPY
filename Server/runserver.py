from Startup import app

from OpenSSL import SSL
# context = SSL.Context(SSL.SSLv23_METHOD)
# context.use_privatekey_file('server.key')
# context.use_certificate_file('server.crt')

# app.run(debug=True)
app.run(host='0.0.0.0',debug = True)
# app.run(host='0.0.0.0',port=5000,debug = True,ssl_context=context)