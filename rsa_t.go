package main

import (
    "fmt"
    "encoding/base64"
    "crypto/rsa"
    "crypto/rand"
)

func Base64Encode(b []byte) []byte {
	tmp := make([]byte, base64.StdEncoding.EncodedLen(len(b)))
	base64.StdEncoding.Encode(tmp, b)
	var ret []byte
	for len(tmp) > 60 {
		ret = append(ret, tmp[:60]...)
		ret = append(ret, ' ')
		tmp = tmp[60:]
	}
	ret = append(ret, tmp...)
	return ret
}

func main(){
    priv, err := rsa.GenerateKey(rand.Reader, 1024)
    if err != nil {
        fmt.Printf("err:%T", err)
    }
    publicN := priv.PublicKey.N.Bytes()
    fmt.Printf("%d", publicN)
    publicN = append([]byte{0}, publicN...)
    fmt.Printf("%d", publicN)
    b := Base64Encode(publicN)
    b = append(b, []byte("AQAB")...)
    fmt.Printf("%s", b)
}
