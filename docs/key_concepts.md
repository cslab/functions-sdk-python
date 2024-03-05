## Webhooks
Webhooks in __CIM Database Cloud__ can be used to call HTTP endpoints with context-related metadata for certain events (e.g. document release).
Further information about webhooks can be found in the CIM Database Cloud documentation.

## Functions

Webhooks can also call **Functions**, which allow execution of custom code in the CIM Database Cloud serverless infrastructure. This allows customers to enhance their CIM Database Cloud experience by implementing their own business logic.

<figure markdown="span">
  ![Overview schema](assets/functions-overview.png)
  <figcaption></figcaption>
</figure>

## Environments
Functions are grouped into **environments**, which are the (Docker) container the code runs in. An environment contains a runtime for its specific programming language, the Function code and a configuration file describing the environment.

If the Functions in an environment have not been executed in a while, the environment will become "cold" and the next start of a Function will take a bit longer. Therefore it is recommended to place all your Functions in the same environment.
