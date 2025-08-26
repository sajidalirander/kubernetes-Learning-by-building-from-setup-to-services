## Converting to Base64
There's a simple command for the encoding. Most Linux systems have a `base64` tool built-in. The trick is to use it correctly with the echo command.

The command looks like this:
```bash
echo -n 'your-secret-key' | base64
```

The most important part of that command is the `-n`. By default, echo adds an invisible newline character at the end of the text. The `-n` flag tells echo not to add that newline. If we didn't use it, the newline would get encoded along with the password, making it incorrect.

You can try it yourself right now with your password:
```bash
sajid@sajid:~$ echo -n 'admin' | base64
YWRtaW4=
sajid@sajid:~$ echo -n 'admin123' | base64
YWRtaW4xMjM=
```
It should give you encoded value, the exact value should be placed in YAML file.

