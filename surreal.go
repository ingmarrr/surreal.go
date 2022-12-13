package main

import (
	"io"
	"net/http"
)

type (
	Response struct {
		Time   string
		Code   int
		Result string
	}

	Client struct {
		cl *http.Client
	}
)

func (c *Client) Get(url string) (*Response, error) {
	resp, err := c.cl.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	return &Response{
		Time:   resp.Header.Get("Date"),
		Code:   resp.StatusCode,
		Result: resp.Status,
	}, nil
}

func (c *Client) Post(url string, bodyType string, body io.Reader) (*Response, error) {
	resp, err := c.cl.Post(url, bodyType, body)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	return &Response{
		Time:   resp.Header.Get("Date"),
		Code:   resp.StatusCode,
		Result: resp.Status,
	}, nil
}
