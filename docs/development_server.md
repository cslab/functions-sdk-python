The Functions SDK includes a development server that allows you to run your Functions in your development environment. The server reads Functions from the `environment.yaml` file in your working directory and makes the Functions available via HTTP endpoints. You can then connect those Functions to your CIM Database Cloud instance using Webhooks.

This speeds up the development of Functions, because you can instantly test your changes, without deploying them to the cloud infrastructure first.

## Starting the Server

You can start the development server using the following command:

```bash
python -m functions.server
```

You can set the port of the server using the `--port` flag (default is 8000), or by setting the `CON_DEV_PORT` environment variable:

```bash
python -m functions.server --port 8080
```

You can set the directory containing the `environment.yaml` file using the `--dir` flag (by default the current working directory is used) or by setting the `CON_DEV_DIR` environment variable:

```bash
python -m functions.server --dir ./my_functions
```

You can enable HMAC verification of requests using the `--secret` flag, or by setting the `CON_DEV_SECRET` environment variable:

```bash
python -m functions.server --secret my_secret
```

## Autoreloading

The development server will automatically restart if you make changes to your Functions code. However it will not restart if you make changes to the `environment.yaml` file.

## Exposing the server

After starting the server, you need to expose the server to the outside world, to enable your CIM Database Cloud instance to send webhook requests to your Functions.
There are multiple ways to do this:

### GitHub Codespaces

If you are developing Functions in a GitHub Codespace you can simply forward the port of the server, by right clicking on the dev servers port in the the "Ports" tab and changing the visibility to "Public":

![GitHub Codespaces](./assets/codespace_port_visibility.png)

You can then copy the URL of the server and use it to connect your Functions to your CIM Database Cloud instance using Webhooks.
The URL of the webhook will be the URL of the forwarded port, combined with the Functions set in the `environment.yaml` file.

For example the `example` function would be available at:

```
https://mycodespace-5g7grjgvrv9h4jrx-8000.app.github.dev/example
```

### ngrok and Cloudflare

If you are developing Functions locally, you can use services like [ngrok](https://ngrok.com/) or [Cloudflare](https://cloudflare.com) to expose the server.

Please refer to the documentation of the specific service for instructions on how to do this.

The URL for the webhook will be the URL of the service, combined with the Functions set in the `environment.yaml` file.

For example the `example` function would be available at:

```
https://my-ngrok-tunnel.ngrok.app/example
```

## Create a webhook in CIM Database Cloud

To test your Functions locally, you can create a webhook in your CIM Database Cloud instance and point it to your development server.

The URL of the webhook will be the URL of the development server, combined with the Functions name set in the `environment.yaml` file using the following format: `https://<development-server-url>/<function-name>`

For example the `example` function would be available at:

```https://mycodespace-5g7grjgvrv9h4jrx-8000.app.github.dev/example```


Make sure to set the webhooks event to the correct event you want to test with your Function.

For more detaikled information on how to create a webhook in CIM Database Cloud, please refer to the [CIM Database Cloud documentation](https://saas-docs.contact-cloud.com/2025.7.0-en/admin/admin-contact_cloud/saas_admin/webhooks).


## Securing the development server

Since the development server is exposed to the outside world, you should secure it to prevent unauthorized access.

You can enable HMAC verification of requests using the `--secret` flag, or by setting the `CON_DEV_SECRET` environment variable:

```bash
python -m functions.server --secret my_secret
```

Make sure to use the same secret in your CIM Database Cloud instance when setting up the webhook and enable HMAC signing.
