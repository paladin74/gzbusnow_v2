package main

import (
	"bytes"
	"crypto/cipher"
	"crypto/des"
	"crypto/rand"
	"crypto/rsa"
	"encoding/base64"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"

//	"./mahonia"
)

var listenAddr = flag.String("listenAddr", ":8999", "listen addr")

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

func Base64Decode(b []byte) ([]byte, error) {
    fmt.Printf("%s", b)
	b = bytes.Replace(b, []byte{' '}, []byte{}, -1)
    fmt.Println("%s", b)
	var d int
	if b[len(b)-2] == '=' {
		d = 2
	} else if b[len(b)-1] == '=' {
		d = 1
	}
	ret := make([]byte, base64.StdEncoding.DecodedLen(len(b)))
	_, err := base64.StdEncoding.Decode(ret, b)
	if err != nil {
		return nil, err
	}
    fmt.Println("%s", ret)
    fmt.Println("%s", ret[:len(ret)-d])
	return ret[:len(ret)-d], nil
}

var iv = []byte{0x01, 0x09, 0x08, 0x02, 0x00, 0x07, 0x00, 0x05}

func PKCS5Padding(b []byte, blockSize int) []byte {
	nPadding := blockSize - len(b)%blockSize
	padding := bytes.Repeat([]byte{byte(nPadding)}, nPadding)
	b = append(b, padding...)
	return b
}

func PKCS5Unpadding(b []byte) []byte {
	nPadding := int(b[len(b)-1])
	return b[:len(b)-nPadding]
}

func DESEncrypt(key []byte, text []byte) ([]byte, error) {
	text = PKCS5Padding(text, des.BlockSize)
	block, err := des.NewCipher(key)
	if err != nil {
		return nil, err
	}
	ciphertext := make([]byte, len(text))
	mode := cipher.NewCBCEncrypter(block, iv)
	mode.CryptBlocks(ciphertext, text)
	return ciphertext, nil
}

func DESDecrypt(key []byte, ciphertext []byte) ([]byte, error) {
	block, err := des.NewCipher(key)
	if err != nil {
		return nil, err
	}
	text := make([]byte, len(ciphertext))
	mode := cipher.NewCBCDecrypter(block, iv)
	mode.CryptBlocks(text, ciphertext)
	return PKCS5Unpadding(text), nil
}

type WoQuery struct {
	desKey []byte
	url    string
}

func (q *WoQuery) Init() error {
	q.url = "http://info.gzyyjt.net:9009/unicom"
	b, err := q.getDESKey()
	if err != nil {
		return err
	}
	q.desKey = b
	return nil
}

func (q *WoQuery) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if r.FormValue("type") == "detail" {
		routeName := r.FormValue("routeName")
		ret, err := q.GetDetail(routeName)
		if err != nil {
			log.Println(err)
			http.Error(w, "", http.StatusInternalServerError)
			return
		}
		w.Write(ret)
	} else if r.FormValue("type") == "fuzzy" {
		routeName := r.FormValue("routeName")
		ret, err := q.GetFuzzy(routeName)
		if err != nil {
			log.Println(err)
			http.Error(w, "", http.StatusInternalServerError)
			return
		}
		w.Write(ret)
	}
}

func (q *WoQuery) genCommonParams() map[string]string {
	return map[string]string{
		"password":  "123456",
		"username":  "android",
		"version":   "2.5.1",
		"devNumber": "000000005E23FE04000000001FBF1D1E0LVUWKLZUR",
		"devType":   "0",
	}
}

func escapeParams(params map[string]string) []byte {
	var buf bytes.Buffer
	for k, v := range params {
		fmt.Fprintf(&buf, "%s=%s&", url.QueryEscape(k), url.QueryEscape(v))
	}
	return buf.Bytes()
}

func (q *WoQuery) GetDetail(name string) ([]byte, error) {
	params := q.genCommonParams()
	params["oper"] = "detail"
	params["type"] = "line"
	params["queryType"] = "1"
	params["routeName"] = name
	return q.DoQuery(q.url+"/Bus", params)
}

func (q *WoQuery) GetFuzzy(name string) ([]byte, error) {
	params := q.genCommonParams()
	params["oper"] = "fuzzy"
	params["type"] = "line"
	params["queryType"] = "1"
	params["routeName"] = name
	return q.DoQuery(q.url+"/Bus", params)
}

func (q *WoQuery) DoQuery(url string, params map[string]string) ([]byte, error) {
	content := escapeParams(params)
	content, err := DESEncrypt(q.desKey, content)
	if err != nil {
		return nil, err
	}
	content = Base64Encode(content)
	resp, err := http.Post(url, "", bytes.NewReader(content))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	b, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}
	b, err = Base64Decode(b)
	if err != nil {
		return nil, err
	}
	b, err = DESDecrypt(q.desKey, b)
	if err != nil {
		return nil, err
	}
	return b, nil
}

func (q *WoQuery) getDESKey() ([]byte, error) {
	priv, err := rsa.GenerateKey(rand.Reader, 1024)
	if err != nil {
		return nil, err
	}
	publicN := priv.PublicKey.N.Bytes()
	publicN = append([]byte{0}, publicN...)
	b := Base64Encode(publicN)
	b = append(b, []byte("AQAB")...) // 65537 base64encoded
	resp, err := http.Post(q.url+"/data", "", bytes.NewReader(b))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	b, err = ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}
	b, err = Base64Decode(b)
	if err != nil {
		return nil, err
	}
	key, err := rsa.DecryptPKCS1v15(rand.Reader, priv, b)
	if err != nil {
		return nil, err
	}
    fmt.Printf("%s", key)
	return key, nil
}

func main() {
	flag.Parse()

	woQuery := new(WoQuery)
	err := woQuery.Init()
	if err != nil {
		log.Fatal(err)
	}
	http.Handle("/", woQuery)
	log.Printf("listening at %s", *listenAddr)
	err = http.ListenAndServe(*listenAddr, nil)
	if err != nil {
		log.Fatal(err)
	}
}
