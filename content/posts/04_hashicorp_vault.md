---
Title: Getting Started with HashiCorp Vault
Date: 2020-07-18
Author: smirza
Slug: hashicorp-vault
Tags: vault, secret-management
Keywords:
Summary: Vault is a secrets management platform. It provides a range of features designed to encrypt secrets, control access to secrets through authentication and authorization, and records secrets access through auditing.
Status: published
---

> Vault is a secrets management platform. It provides a range of features designed to encrypt secrets, control access to secrets through authentication and authorisation, and records secrets access through auditing.

![/static/img/posts/06_hash-vault01/img1.png](/static/img/posts/06_hash-vault01/img1.png)

## Why use Vault ?

Vault’s architecture is composed of several internal components. These components are used to get data in and out of Vault. Vault offers features that support secrets management. Many enterprises keep secrets distributed across many systems, databases, configuration files, continuous integration systems, and source control. Vault can manage all the secrets of an enterprise from a single system. This makes it very easy to control and audit all access to secrets and revoke secrets when necessary. Vault provides internal encryption capabilities and encryption is a service to users and systems. TLS connections are required to access a production Vault server. This encrypts the secrets over the wire, so they cannot be intercepted. Vault includes support for external identity management providers. Vault uses policies to control access to secrets, and Vault has the capability to audit all secrets access.

## What is a Secret ?

Technically, a secret is any data we want to keep confidential. Vault is capable of storing any secret such as a credit card number or driver’s license number. However, the primary use case for Vault is to protect what we might call operational secrets, the secrets that tie our systems together. A database password is a perfect example. Most databases support username and password authentication. A username-password combination is used by an application to authenticate to the database. These secrets are often stored in configuration files, which are then stored in source control. These persistent secrets are long lived, distributed all over an enterprise, and are prone to loss.

## Vault Components

Vault provides a server process and API used to store these types of secrets. Its internal architecture ensures that secrets exist only as long as necessary. A production Vault server never stores or transmits secrets in plain text. Rather than storing secrets in files where they may be compromised, secrets are stored using Vault.

Users and applications that need those secrets request them from Vault. Vault includes three primary components.

- Vault CLI - Used primarily for setup and administration.
- Vault Server - Process that handles all client requests for setup, configuration, and secret access.
- Vault API - Vault offers a rich HTTP API for all functions. Applications and systems integration with Vault should be through the API.

Every function supported by the command line interface has an associated HTTP API, however, some APIs have no CLI command

## Vault Cryptography

Cryptography is used to keep secrets safe both in transit and in permanent storage also known as at rest. The only storage medium that should ever store unencrypted data is system memory, and only for as long as necessary.

### In Transit

Vault uses two essential cryptographic techniques to protect data. The Vault API uses Transport Layer Security (TLS) to encrypt data over the wire between Vault and http clients. Vault uses TLS to ensure that all communications between a Vault server and a client are encrypted. TLS uses an asymmetric algorithm in which one key is used to encrypt data and a different key is used to decrypt.

### Encryption at rest (within the Vault - Internally)

Vault uses the Advanced Encryption Standard to encrypt data internally - AES256. AES uses a symmetric encryption algorithm which means that a single key is used to encrypt and decrypt data. Vault uses AES because it is considered to be highly secure and because symmetric encryption algorithms are considerably faster than asymmetric. AES256, the AES variant used by Vault, encrypts data in 256 blocks. Symmetric algorithms use a single key to both encrypt and decrypt data.

A single master encryption key can decrypt all data within a Vault server. This single key can be used to access all the secrets within Vault so it must also be protected.

Vault uses a key sharding technique called Shamir’s Secret Sharing. This is a mathematical method for splitting a secret into shards such that a minimum number of shards called a quoram is required to reconstruct the secret. In this case the secret is the master key itself. When a Vault server is started, it generates a new master key. That key is never stored or even displayed. Instead the shards are output to the console.

Using Shamir’s Secret Sharing, operators of Vault can implement the two man rule. No one person is ever allowed access to more than one shard. Individually, the shards are worthless. Only when combined are they able to reconstruct the master key and unseal a Vault server.

## Vault concepts and architecture

Vault is provided as a single executable. The executable runs a Vault server and provides a command-line interface to a running Vault server. The Vault server also exposes an HTTP API that clients can use to interact with Vault.

Architectural Components of Vault:  
![/static/img/posts/06_hash-vault01/img2.png](/static/img/posts/06_hash-vault01/img2.png)

This diagram is a simple representation of the internal components of Vault:  
![/static/img/posts/06_hash-vault01/img3.png](/static/img/posts/06_hash-vault01/img3.png)

One important thing to understand is that Vault does not itself actually store any data. Vault’s job is to securely encrypt data and then rely on an external system to store that data. Vault supports several storage backends, which store Vault data and secrets. Vault also needs a store (storage) for its own operational data, including tokens, policies, and system data.

### Storage Backend

Vault supports several storage backends, including local file systems, key value stores including HashiCorp Consul and etcd, cloud-based storage, and relational databases such as MySQL and Postgres. Vault’s configuration determines which of these backends is used. Durable storage backends never see unencrypted data, so if a Vault backend is compromised, the data is unreadable without the Vault server to decrypt the data. HashiCorp directly supports some of these backends, such as Consul. Others, such a etcd and relational databases, are community-supported.

Each backend has benefits and trade-offs, such as how they’re supported and how they support capabilities such as high-availability. All the components inside Vault, the logic that handles secrets, authentication, and authorization, are inside a virtual barrier. Vault’s architecture ensures that unencrypted data never enters or leaves the barrier through the HTTP API or between Vault and the storage backends. Thus, data going through Vault is protected by Vault, both in transit and at rest, at all times. Applications and users access Vault through the API directly or through the Vault CLI. Internal backend components communicate between Vault and the storage backends.

### Secret Engine

Vault provides several mechanisms to store secrets. Vault adapts to different types of secrets using a pluggable implementation architecture. Vault includes a set of secrets engines, each of which provides storage and interaction implementations specific to the types of secrets they’re designed to handle. For example, the generic, all-purpose KV secrets engine stores secrets in key value pairs. Dynamic secrets engines, such as SSH and Database, generate secrets on-demand. Developers can also write custom secrets engines and plug them into Vault to handle specialised use cases.

### Authentication Methods

Vault production servers always start in a sealed state. A sealed Vault server is almost completely unusable. The server must be unsealed to accept authentication requests and allow access to stored secrets. When a Vault server is started, a master key is generated and split into five shards. The operator starting the server can configure the server to require all or only some of the shards to unseal the Vault server. This technique ensures that the entire master key is never stored in a single place. The shards can be distributed to multiple operators so that unsealing the Vault requires the cooperation of multiple operators. When it comes to sealing a Vault server, however, a single operator can do that. In the event of an emergency, the Vault server can quickly be sealed by a single operator to prevent further data loss.

Vault can integrate with authentication platforms such as LDAP, Active Directory, and third-party identity providers such as GitHub and AWS. Non-human users, such as applications, are authenticated to Vault using a method called AppRole. This includes business systems that require secrets access and continuous integration tools that build and deploy software. Regardless reds of the integrated authentication method used by Vault, a successful authentication request always returns a token. The token authentication method actually allows read and write access to secrets depending on the permissions granted by the token. The permissions are determined by policies.

Tokens are a method for authentication to Vault. Every token comes issued with a lease. Leases don’t live forever, they have a time to live, or TTL, which determines how long the token has access to secrets. When the lease TTL is up, Vault expires the token by revoking it. Administrators can also revoke tokens manually using the CLI or API. Tokens can also be issued with a limited number of uses. Leases force clients to periodically authenticate to Vault to maintain access to secrets. This prevents long-lived secrets from being used to compromise data security. A token can be associated with one or more policies.

Policies determine the secrets a token can access and whether that token can be used to read or write secrets to a path in Vault. Vault policy definition files can be uploaded by the CLI or the API. Tokens and policies are used together to implement role-based access control to secrets. Policies are associated with tokens when they are generated. The precise mechanism for this depends on the authentication method being used.

### Auditing

Auditing access to secrets is a common security requirement. Vault can also create an audit record of every usage of every token in the system. When enabled, audit devices store a record of each access to a secret and any errors related to secrets access. Vault treats auditing as part of a secrets access transaction. If auditing is enabled, any failure in recording an audit record will cause a secrets access request to fail. This prevents a bad actor from covering tracks by compromising the audit record of a secrets access.

## Using the Dev Server

A Vault server running in dev mode is useful for testing and experimentation. Dev mode servers differ from production servers.

- A dev server is meant for experimentation and testing only, never for production use.
- TLS is disabled, so secrets are not encrypted in transit.
- The dev server uses an in-memory storage back end.
- A Vault dev server starts unsealed.
- Displays the entire unseal key. (The command to start a dev server displays a single unsealed key rather than key shards)

To start a dev environment

```bash
$ vault server -dev
==> Vault server configuration:

             Api Address: http://127.0.0.1:8200
                     Cgo: disabled
         Cluster Address: https://127.0.0.1:8201
              Go Version: go1.13.12
              Listener 1: tcp (addr: "127.0.0.1:8200", cluster address: "127.0.0.1:8201", max_request_duration: "1m30s", max_request_size: "33554432", tls: "disabled")
               Log Level: info
                   Mlock: supported: false, enabled: false
           Recovery Mode: false
                 Storage: inmem
                 Version: Vault v1.4.3

WARNING! dev mode is enabled! In this mode, Vault runs entirely in-memory
and starts unsealed with a single unseal key. The root token is already
authenticated to the CLI, so you can immediately begin using Vault.

You may need to set the following environment variable:

    $ export VAULT_ADDR='http://127.0.0.1:8200'

The unseal key and root token are displayed below in case you want to
seal/unseal the Vault or re-authenticate.

Unseal Key: QGIjkWVB2rXFq9K5yrLRuAxmtKwgN47c2tiX2ruSBdo=
Root Token: s.heERPfskm0Vsjvv570I61tIO

Development mode should NOT be used in production installations!

==> Vault server started! Log data will stream in below:
```

This will start a new Vault server in dev mode, display status information, and block. Some important elements of the output.

`Api Address:` it is the URL where requests can be sent to the running Vault server. This is how the CLI and other applications can communicate with Vault.

`Cluster Address:` The cluster address is used when a Vault server is part of a high availability cluster.

`Mlock:` Mlock is a Linux feature that prevents memory from being swapped to disc. When enabled, this prevents unencrypted secrets in memory from being written to permanent storage.

`Storage:` Storage is the back end used by Vault. The dev server uses an in-mem or in-memory storage back end.

These lines list the information we need to interact with Vault, the unseal key and the root token. The unseal key of a dev server is the entire master key for this Vault server. The root token is a special token used for administration of the Vault server.

```bash
Unseal Key: QGIjkWVB2rXFq9K5yrLRuAxmtKwgN47c2tiX2ruSBdo=
Root Token: s.heERPfskm0Vsjvv570I61tIO
```

In order to execute commands on this server, we’ll need to open a second terminal window. Do that and then execute this command.

`export VAULT_ADDR='http://127.0.0.1:8200'`

This command sets an environment variable used by the Vault CLI. The CLI checks this variable to get the address of the running Vault server. Vault servers listen on port 8200 by default.

Congratulations, you’ve just started your first Vault server.

## Vault Status

This command gets information about the current state of the vault server. This server is running and is technically using Shamir’s Secret Sharing to protect the master key, even though the the key of a dev server is not split into shards.

```bash
$ vault status
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    1
Threshold       1
Version         1.4.3
Cluster Name    vault-cluster-8876c4f3
Cluster ID      cc785870-45db-0af4-f24a-3063ee554297
HA Enabled      false
```

## First Secret

Our first demonstration of Vault will be to write a simple key value pair to the KV secrets engine.

```bash
$ vault kv put secret/mySecret password=myPassword
Key              Value
---              -----
created_time     2020-07-17T08:26:49.858224Z
deletion_time    n/a
destroyed        false
version          1
```

The Vault KV command interacts with the KV secrets engine. Vault KV put adds a new secret at the path secret/mySecret. The secret is a key value pair. The key is password and the value is myPassword. The output returns metadata about the secret that we just created, including the creation time. Our secret is now stored in memory in the vault server and encrypted.

Let’s now read the secret back out of Vault.

```bash
vault kv get secret/mySecret
====== Metadata ======
Key              Value
---              -----
created_time     2020-07-17T08:26:49.858224Z
deletion_time    n/a
destroyed        false
version          1

====== Data ======
Key         Value
---         -----
password    myPassword
```

The output of this command is the secret metadata and the secret itself. We can also return the data in JSON format. This is the format Vault would use to respond to an HTTP API request.

```bash
vault kv get -format=json secret/mySecret
{
  "request_id": "59561698-903d-81f6-c900-c0d1ab483344",
  "lease_id": "",
  "lease_duration": 0,
  "renewable": false,
  "data": {
    "data": {
      "password": "myPassword"
    },
    "metadata": {
      "created_time": "2020-07-17T08:26:49.858224Z",
      "deletion_time": "",
      "destroyed": false,
      "version": 1
    }
  },
  "warnings": null
}
```

---

## Introduction to Vault Secrets Engines

Vault is designed to be a general-purpose secrets management solution. It supports arbitrary secrets with Key/Value stores, and other, more specialized secrets (Cloud, Github, Cubbyhole, SSH, Database, token , nomad, and more). In each case Vault writes, updates, reads, and deletes secrets from storage back ends. It authenticates access to the secrets, and controls permissions to those secrets.

**Vaults Virtual File System**
Reading, writing, and deleting data to a secured location in a system may sound familiar. If this sounds like a file system, there’s a good reason. Vault uses a virtual file system paradigm to provide access to secrets starting with paths. Vault mounts a secrets engine, somewhat like a hard drive, to a path when it is enable. Some secrets engines are enabled by default when a new Vault server is initialized. The others must be enabled by an administrator before they can be used.

![/static/img/posts/06_hash-vault01/3956E653-80D1-4FB6-BEC7-323B78CC3A0A.png](/static/img/posts/06_hash-vault01/3956E653-80D1-4FB6-BEC7-323B78CC3A0A.png)

**Secrets Engine Paths**

The first section of these paths are secrets engines that are mounted to a Vault server. The elements after the first slash relate to predefined paths within the secrets engines, and the secrets stored within them.

![/static/img/posts/06_hash-vault01/DFFEBB63-18AB-4656-A28A-0B7B93F7CDC4.png](/static/img/posts/06_hash-vault01/DFFEBB63-18AB-4656-A28A-0B7B93F7CDC4.png)

Here are some examples of commands that work with paths.

**Enabling a Secrets Engine** `vault secrets enable database`
This command mounts the database secrets engine to a path called database.

**Writing to a Path** `vault write database/config/mysql_app1`
This command writes a secret to the database secrets engine. The database portion of the path is the engine itself, like a drive. Config is a path built into the secrets engine. Mysql_app1 is the secret, which contains values specific to this path.

**Mpunting a secrets engine to a path** `vault secrets enable -path=myAppDB database`
You can create multiple mounts of the same secrets engine. This command mounts the database engine to a different path, called myAppDB. The secrets stored in this mount are isolated from other mounts. This gives you a lot of flexibility in storing and securing secrets for a wide variety of use cases.

**Writing to the database secrets engine** `vault write myAppDB/confid/mysql_app1`
This last command writes a secret to the myAppDB secrets engine mount created in the previous command. So secrets engines are purpose built, secrets management implementations, exposed in a familiar virtual file system scheme.

Each secrets engine has its own specialized way of reading, writing, and controlling access to secrets. Secrets engine are isolated from each other and can not read each other’s secrets.

---

## Working with Vault secrets engines

Vault Secret List

```bash
$ vault secret list
Path          Type         Accessor              Description
----          ----         --------              -----------
cubbyhole/    cubbyhole    cubbyhole_3614db8d    per-token private secret storage
identity/     identity     identity_75715818     identity store
secret/       kv           kv_45676b03           key/value secret storage
sys/          system       system_4c42b690       system endpoints used for control, policy and debugging
```

The **cubbyhole** secrets engine is a variant of the KV secrets engine. Cubbyhole access is scoped by token, which means that a cubbyhole token can only read one cubbyhole, and each cubbyhole has only one valid token. When a cubbyhole token expires, the cubbyhole is destroyed.

The **identity** secrets engine is built into the vault, and is the basis for vault authentication.

The **secret** secrets engine is the generic KV secret storage. Note that the type is listed as KV. This is the secrets engine accessed by the vault KV put command.

The **sys** secrets engine is the engine used by vault to manage vault itself. This engine is used for vault administration, such as generating a new root key, or unsealing a vault server.

These secrets engines are enabled by default when a new vault server is started. With the exception of the secret KV engine, they cannot be disabled or moved.

```bash
$ vault secrets enable -path=myApp kv
Success! Enabled the kv secrets engine at: myApp/
```

The above command enables the KV secrets engine on a new path called my app. Now execute `vault secrets list` again.

```bash
$ vault secrets list
Path          Type         Accessor              Description
----          ----         --------              -----------
cubbyhole/    cubbyhole    cubbyhole_3614db8d    per-token private secret storage
identity/     identity     identity_75715818     identity store
myApp/        kv           kv_a93a5c56           n/a
secret/       kv           kv_45676b03           key/value secret storage
sys/          system       system_4c42b690       system endpoints used for control, policy and debugging
```

You’ll see that there are now two listings under path where the type is KV, the original default secrets path, and the new my app path we just enabled. Let’s execute vault KV put my app forward slash my other secret space key equals value.

```Bash
$ vault kv put myApp/myOtherSecret key=value
Success! Data written to: myApp/myOtherSecret
```

We’ve just written a new secret, and now we can get it back out

```bash
$ vault kv get myApp/myOtherSecret
=== Data ===
Key    Value
---    -----
key    value
```

These commands store a new secret on the my app path and retrieve the secret. You can use this mechanism to create isolated stores of secrets to accommodate any storage scheme that makes sense for your particular use case. For example, you could create stores that align to your company’s organizational structure, or you could dedicate stores to application groups.

You can get information about the paths supported by a secrets engine by executing this command:

```bash
$ vault path-help secret ### where secret is the secret engine
## DESCRIPTION

This backend provides a versioned key-value store. The kv backend reads and
writes arbitrary secrets to the storage backend. The secrets are
encrypted/decrypted by Vault: they are never stored unencrypted in the backend
and the backend never has an opportunity to see the unencrypted value. Each key
can have a configured number of versions, and versions can be retrieved based on
their version numbers.

## PATHS

The following paths are supported by this backend. To view help for
any of the paths below, use the help command with any route matching
the path pattern. Note that depending on the policy of your auth token,
you may or may not be able to access certain paths.

    ^.*$


    ^config$
        Configures settings for the KV store

    ^data/(?P<path>.*)$
        Write, Read, and Delete data in the Key-Value Store.

    ^delete/(?P<path>.*)$
        Marks one or more versions as deleted in the KV store.

    ^destroy/(?P<path>.*)$
        Permanently removes one or more versions in the KV store

    ^metadata/(?P<path>.*)$
        Configures settings for the KV store

    ^undelete/(?P<path>.*)$
        Undeletes one or more versions from the KV store.
```

help command displays detailed information about the paths supported by a secrets engine. This is the list of paths supported by the secret, or KV secrets engine. Each path listing is a regular expression that defines the structure of the path.

In order to get help for a secrets engine path, the secrets engine must be enabled.

```bash
$ vault secrets enable database
Success! Enabled the database secrets engine at: database/
```

```bash
$ vault secrets list
Path          Type         Accessor              Description
----          ----         --------              -----------
cubbyhole/    cubbyhole    cubbyhole_3614db8d    per-token private secret storage
database/     database     database_2083f39a     n/a
identity/     identity     identity_75715818     identity store
myApp/        kv           kv_a93a5c56           n/a
secret/       kv           kv_45676b03           key/value secret storage
sys/          system       system_4c42b690       system endpoints used for control, policy and debugging
```

Now we can execute vault path-help database.

```bash
$ vault path-help database
## DESCRIPTION

The database backend supports using many different databases
as secret backends, including but not limited to:
cassandra, mssql, mysql, postgres

After mounting this backend, configure it using the endpoints within
the "database/config/" path.

## PATHS

The following paths are supported by this backend. To view help for
any of the paths below, use the help command with any route matching
the path pattern. Note that depending on the policy of your auth token,
you may or may not be able to access certain paths.

    ^config/(?P<name>\w(([\w-.]+)?\w)?)$
        Configure connection details to a database plugin.

    ^config/?$
        Configure connection details to a database plugin.

    ^creds/(?P<name>\w(([\w-.]+)?\w)?)$
        Request database credentials for a certain role.

    ^reset/(?P<name>\w(([\w-.]+)?\w)?)$
        Resets a database plugin.

    ^roles/(?P<name>\w(([\w-.]+)?\w)?)$
        Manage the roles that can be created with this backend.

    ^roles/?$
        Manage the roles that can be created with this backend.

    ^rotate-role/(?P<name>\w(([\w-.]+)?\w)?)$
        Request database credentials for a certain role.

    ^rotate-root/(?P<name>\w(([\w-.]+)?\w)?)$
        Request database credentials for a certain role.

    ^static-creds/(?P<name>\w(([\w-.]+)?\w)?)$
        Request database credentials for a certain static role. These credentials are
        rotated periodically.

    ^static-roles/(?P<name>\w(([\w-.]+)?\w)?)$
        Manage the static roles that can be created with this backend.

    ^static-roles/?$
        Manage the static roles that can be created with this backend.
```

We can see that the database secrets engine supports a different set of paths than the secret secrets engine. These paths support the function of the database secrets engine. The database secrets engine allows vault to manage authentication to supported databases. Again, each listing is a regular expression that describes the format of the supported path.

We can go one step further, vault path dash help database forward slash roles, where roles is one of the supported paths in the database secrets engine. This command displays more detailed information about the roles path within the database secrets engine. You can use path dash help this way to learn more about a secrets engine.

```bash
$ vault path-help database/roles
Request:        roles
Matching Route: ^roles/?$

Manage the roles that can be created with this backend.


## DESCRIPTION

This path lets you manage the roles that can be created with this backend.

The "db_name" parameter is required and configures the name of the database
connection to use.

The "creation_statements" parameter customizes the string used to create the
credentials. This can be a sequence of SQL queries, or other statement formats
for a particular database type. Some substitution will be done to the statement
strings for certain keys. The names of the variables must be surrounded by "{{"
and "}}" to be replaced.

  * "name" - The random username generated for the DB user.

  * "password" - The random password generated for the DB user.

  * "expiration" - The timestamp when this user will expire.

Example of a decent creation_statements for a postgresql database plugin:

	CREATE ROLE "{{name}}" WITH
	  LOGIN
	  PASSWORD '{{password}}'
	  VALID UNTIL '{{expiration}}';
	GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "{{name}}";

The "revocation_statements" parameter customizes the statement string used to
revoke a user. Example of a decent revocation_statements for a postgresql
database plugin:

	REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM {{name}};
	REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM {{name}};
	REVOKE USAGE ON SCHEMA public FROM {{name}};
	DROP ROLE IF EXISTS {{name}};

The "renew_statements" parameter customizes the statement string used to renew a
user.
The "rollback_statements' parameter customizes the statement string used to
rollback a change if needed.
```

---

## Vault Authentication

Every request to a Vault server to retrieve a secret must be authenticated. Vault validates the identity of the caller, then returns a token. Tokens are used to access secrets involved. All successful authentication requests return a token. Vault provides a number of authentication methods. Here are a few of the available methods.

- Userpass - Username/Password
- Active Directory and LDAP
- Cloud Providers - Azure, AWS and GCP
- GitHub

**Non-human Authentication:**

- AppRole
  > AppRole is used by applications and automation tools to authenticate to Vault.
- Kubernetes
  > Which authenticates to Vault using a Kubernetes service account token.

Each of these methods has a path involved and must be enabled individually. The token returned by these methods are limited use keys that are associated with the user, possibly a group and with a policy which determines the secrets that are readable or writable by the token.

Userpass is useful for testing and compatibility purposes. It’s not the best option for a production vault server. The passwords you set on users are secrets themselves. If you use the userpass authentication method you’ll need a method to protect those secrets outside of Vault. The other methods such as Active Directory or GitHub are better suited to production Vault servers.

List the authentication methods that are currently available by

```bash
$ vault auth list
Path      Type     Accessor               Description
----      ----     --------               -----------
token/    token    auth_token_b9cc64eb    token based credentials
```

Token method is currently enabled. Next we enable the user pass auth method.

```bash
$ vault auth enable userpass
Success! Enabled userpass auth method at: userpass/
```

We create a new user called `vaultuser` with password as vault.

```bash
 $ vault write auth/userpass/users/vaultuser password=vault
Success! Data written to: auth/userpass/users/vaultuser
```

Login with the username and password created. Returns a metadata as shown below.

```bash
 $ vault login -method=userpass username=vaultuser password=vault
Success! You are now authenticated. The token information displayed below
is already stored in the token helper. You do NOT need to run "vault login"
again. Future Vault requests will automatically use this token.

Key                    Value
---                    -----
token                  s.G0SGJnDiu13b6kKUGptQBbT4
token_accessor         kHGppTdFrTsfCSDC9PbNYSgL
token_duration         768h
token_renewable        true
token_policies         ["default"]
identity_policies      []
policies               ["default"]
token_meta_username    vaultuser
```

We can login directly with the token like

```bash
$ vault login s.G0SGJnDiu13b6kKUGptQBbT4
Success! You are now authenticated. The token information displayed below
is already stored in the token helper. You do NOT need to run "vault login"
again. Future Vault requests will automatically use this token.

Key                    Value
---                    -----
token                  s.G0SGJnDiu13b6kKUGptQBbT4
token_accessor         kHGppTdFrTsfCSDC9PbNYSgL
token_duration         767h57m6s
token_renewable        true
token_policies         ["default"]
identity_policies      []
policies               ["default"]
token_meta_username    vaultuser
```

This is similar to login in with the username and password.

Let us now try login in with the root token and try something new.

```bash
$ vault login s.heERPfskm0Vsjvv570I61tIO
Success! You are now authenticated. The token information displayed below
is already stored in the token helper. You do NOT need to run "vault login"
again. Future Vault requests will automatically use this token.

Key                  Value
---                  -----
token                s.heERPfskm0Vsjvv570I61tIO
token_accessor       RZsmu8SS7K6mOsYIBogpMtbE
token_duration       ∞
token_renewable      false
token_policies       ["root"]
identity_policies    []
policies             ["root"]
```

The token duration is infinite and token does not need to be renewable as it never expires. We can create new token while we are logged in with the root token.

```bash
$ vault token create
Key                  Value
---                  -----
token                s.ByrIvaUtL7bS0dFeJiQjhOJh
token_accessor       qfTlXb1KX91SbIHrFSYAlTIO
token_duration       ∞
token_renewable      false
token_policies       ["root"]
identity_policies    []
policies             ["root"]
```

This generates a new token with the same privileges as the previous one. The new token is now a child of the root token that we used to log in. We can create as many new tokens from this current token as we like. By default, if a parent token is revoked all of its children are also revoked. This makes it easy to revoke a chain of tokens created from a single parent. It’s also possible to create orphan tokens that are not revoked when their parent is revoked for use cases where that is necessary. Now let’s take a look at token accessors.

```bash
$ vault list auth/token/accessors
Keys
----
RZsmu8SS7K6mOsYIBogpMtbE
kHGppTdFrTsfCSDC9PbNYSgL
qfTlXb1KX91SbIHrFSYAlTIO
```

These are all the accessors of the tokens that we’ve created. Accessors can be used to manage a token without actually having that token. Vault administrators and automation systems can use token accessors to renew and revoke token leases. We can also use them to look up a token.

```bash
$ vault token lookup -accessor qfTlXb1KX91SbIHrFSYAlTIO
Key                 Value
---                 -----
accessor            kHGppTdFrTsfCSDC9PbNYSgL
creation_time       1594981574
creation_ttl        768h
display_name        userpass-vaultuser
entity_id           8aacb18e-812a-c727-3cff-fbb231ddd633
expire_time         2020-08-18T15:56:14.865072+05:30
explicit_max_ttl    0s
id                  n/a
issue_time          2020-07-17T15:56:14.865076+05:30
meta                map[username:vaultuser]
num_uses            0
orphan              true
path                auth/userpass/login/vaultuser
policies            [default]
renewable           true
ttl                 767h48m11s
type                service
```

we get information about the token this accessor describes. Here’s the accessor, the creation time of the token, the name of the token’s user, in this case this is the Vault user that we just created, and the policies assigned. This is default because we didn’t associate any policies with the user when we created it. We can also use the CLI to revoke this token.

```bash
$ vault token revoke -accessor kHGppTdFrTsfCSDC9PbNYSgL
Success! Revoked token (if it existed)
```

We can also create a token with a time to live.

```bash
$ vault token create --ttl=5m
Key                  Value
---                  -----
token                s.KTXOHFXxafPWf4bkvR8crFSZ
token_accessor       5aNaGNy1ayZB5Grpl84I8F4T
token_duration       5m
token_renewable      true
token_policies       ["root"]
identity_policies    []
policies             ["root"]
```

This creates a new token with a time to live off five minutes. If we were to wait six minutes and attempt to use this token it will have been revoked by Vault. You’ll notice in the information here output that the token renewable is set to true. This means that if we renew the token using the token itself or its accessor within that five minute window we can extend the life of the token.

---

## Vault Policies

Policies perform authorization on an authenticated request. Secrets are accessed in Vault using a token. A root token is a special token that never expires and can access all paths in a Vault server. Policies can be automatically associated with tokens issued to a single user or groups of users.

The way that a policy is applied to a token depends on the authentication method used to retrieve the token. Authentication methods that support policy mapping can be configured by writing that configuration to Vault. Vault uses HashiCorp Configuration Language, a JSON compatible format, to define policies. They can be uploaded to a Vault server using the CLI or the associated API.

Policies are denied by default which means that permissions must be explicitly granted.

Vault policies grant capabilities to a path. Create, read, update, delete, and list are all capabilities that can be granted to a token. **Sudo** grants access to paths that are root protected. This is typically reserved for administrative level access to a Vault component or secrets engine. **Deny** explicitly denies a capability. Tokens can be generated associated with multiple policies. If a capability is set to deny within any policy associated within a token, that capability is denied regardless of the contents of any other associated policy.

- Create (POST/PUT)
- Read (GET)
- update (POST/PUT)
- Delete (DELETE)
- List (LIST)
- sudo
- deny

**Built-In Policies**

Vault includes two built-in policies

- root - The root policy has sudo access to everything in Vault including sys paths. The only exception is that a root token cannot read a secret stored in a cubbyhole.
- default - includes capabilities that allow tokens to read their own metadata. The default policy can be modified if desired.

**Example Policies**

`app-policy.hcl`

```bash
path "secret/dev" {
	capabilities = ["read"]
}
```

`dev-policy.hcl`

```bash
path "secret/dev" {
	capabilities = ["create", "update", "read", "list"]
}
```

Policy that grants read access to a path. All policies are associated with a path and the policy defines the capabilities granted to that path. This policy might be granted to a token issued to an application. The only permission it grants the application is to read secrets from one path, secret/dev. The application would not be able to access any other paths, create any new secrets, or modify existing secrets within secret/dev. The next example here grants capabilities to the same path as before. However, this one grants additional capabilities. This policy could be used to generate tokens for the development team or Vault admins so they can write secrets to the secret/dev path. Tokens associated with this policy would be able to write secrets to the secret/dev path where the application token can retrieve them.

`vault policy list` lists out the policy that are enabled.

```bash
$ vault policy list
default
root
```

Vault policy read default. This exports the entire default policy. Most of the capabilities listed here have to do with the token managing itself. You can read the comments associated with the capabilities to get more information. Now let’s upload our policies.

```bash
$ vault policy read default
# Allow tokens to look up their own properties
path "auth/token/lookup-self" {
    capabilities = ["read"]
}

# Allow tokens to renew themselves
path "auth/token/renew-self" {
    capabilities = ["update"]
}

# Allow tokens to revoke themselves
path "auth/token/revoke-self" {
    capabilities = ["update"]
}

# Allow a token to look up its own capabilities on a path
path "sys/capabilities-self" {
    capabilities = ["update"]
}

# Allow a token to look up its own entity by id or name
path "identity/entity/id/{{identity.entity.id}}" {
  capabilities = ["read"]
}
path "identity/entity/name/{{identity.entity.name}}" {
  capabilities = ["read"]
}


# Allow a token to look up its resultant ACL from all policies. This is useful
# for UIs. It is an internal path because the format may change at any time
# based on how the internal ACL features and capabilities change.
path "sys/internal/ui/resultant-acl" {
    capabilities = ["read"]
}

# Allow a token to renew a lease via lease_id in the request body; old path for
# old clients, new path for newer
path "sys/renew" {
    capabilities = ["update"]
}
path "sys/leases/renew" {
    capabilities = ["update"]
}

# Allow looking up lease properties. This requires knowing the lease ID ahead
# of time and does not divulge any sensitive information.
path "sys/leases/lookup" {
    capabilities = ["update"]
}

# Allow a token to manage its own cubbyhole
path "cubbyhole/*" {
    capabilities = ["create", "read", "update", "delete", "list"]
}

# Allow a token to wrap arbitrary values in a response-wrapping token
path "sys/wrapping/wrap" {
    capabilities = ["update"]
}

# Allow a token to look up the creation time and TTL of a given
# response-wrapping token
path "sys/wrapping/lookup" {
    capabilities = ["update"]
}

# Allow a token to unwrap a response-wrapping token. This is a convenience to
# avoid client token swapping since this is also part of the response wrapping
# policy.
path "sys/wrapping/unwrap" {
    capabilities = ["update"]
}

# Allow general purpose tools
path "sys/tools/hash" {
    capabilities = ["update"]
}
path "sys/tools/hash/*" {
    capabilities = ["update"]
}

# Allow checking the status of a Control Group request if the user has the
# accessor
path "sys/control-group/request" {
    capabilities = ["update"]
}
```

To upload our policies

`vault policy write dev-policy app-policy.hcl`

`vault policy write app-policy app-policy.hcl`

Vault policy write dev-policy will be the name and then dev-policy.hcl is the file that contains the policy. Once again vault policy write app-policy app-policy.hcl will upload our app policy. And our policies are now uploaded.

```bash
$ vault policy write dev-policy app-policy.hcl
Success! Uploaded policy: dev-policy
$ vault policy write dev-policy dev-policy.hcl
Success! Uploaded policy: dev-policy
```

Vault Policy list show all the new policies in place

```bash
$ vault policy list
app-policy
default
dev-policy
root
```

Create new userpass (ensure the user pass auth methods is enabled - `vault auth enable userpass`) users dev and app and associate the policies that we created with them

```bash
$ vault write auth/userpass/users/dev password=dev policies=dev-policy
Success! Data written to: auth/userpass/users/dev
$ vault write auth/userpass/users/app password=app policies=app-policy
Success! Data written to: auth/userpass/users/app
```

To see the policies attached to a user that we have created:

```bash
$ vault login -method=userpass password=dev username=dev
Success! You are now authenticated. The token information displayed below
is already stored in the token helper. You do NOT need to run "vault login"
again. Future Vault requests will automatically use this token.

Key                    Value
---                    -----
token                  s.DeaHrVY7C11DryuM53geo0A3
token_accessor         vGHGsq8JuL5mMWPlVqlB7ssh
token_duration         768h
token_renewable        true
token_policies         ["default" "dev-policy"]
identity_policies      []
policies               ["default" "dev-policy"]
token_meta_username    dev
```

Check the capabilities of the user against the path:

```bash
$ vault token capabilities secret/data/dev/
create, list, read, update
```

Let us insert a key value into the path:

```bash
vault kv put secret/dev/appsecret user=dbUser
Key              Value
---              -----
created_time     2020-07-17T12:00:39.153233Z
deletion_time    n/a
destroyed        false
version          1
```

Let us now login using a different username (dev - user is associated with the app-policy):

```bash
$ vault login -method=userpass password=app username=app
Success! You are now authenticated. The token information displayed below
is already stored in the token helper. You do NOT need to run "vault login"
again. Future Vault requests will automatically use this token.

Key                    Value
---                    -----
token                  s.Hf1MfDvMtQG4cB1QvnNXV9Vs
token_accessor         5SQ0HlWhDh0zREKa1ff5FM2H
token_duration         768h
token_renewable        true
token_policies         ["app-policy" "default"]
identity_policies      []
policies               ["app-policy" "default"]
token_meta_username    app
```

Let us try reading the key value that we previously inserted with the user dev

```bash
$ vault kv get secret/dev/appsecret
====== Metadata ======
Key              Value
---              -----
created_time     2020-07-17T12:00:39.153233Z
deletion_time    n/a
destroyed        false
version          1

==== Data ====
Key     Value
---     -----
user    dbUser
```

The dev user only has read access to the path, if we try and create a new kv under the path we will get a permission denied as per the policy:

```bash
vault kv put secret/dev/other k=v
Error writing data to secret/data/dev/other: Error making API request.

URL: PUT http://127.0.0.1:8200/v1/secret/data/dev/other
Code: 403. Errors:

* 1 error occurred:
        * permission denied
```

### Conclusion

As the product teams and infrastructure grow, Vault’s extensibility ensures that adding different technologies, environments, and sources of identities integrate seamlessly to allow for fast adoption and increased productivity.
