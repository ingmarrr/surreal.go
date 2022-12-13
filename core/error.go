package core

import "fmt"

type ErrorKind int

const (
	TimeoutError ErrorKind = iota
	Authentication
	Initialization
	DuplicateRequestID
	Query
	ParseError
	Socket
	InvalidSyntax
	InvalidRequest
	InvalidParams
	InternalError
)

func (k *ErrorKind) WithMessage(msg string) *Error {
	return &Error{
		Kind:    *k,
		Message: msg,
	}
}

func (k *ErrorKind) WithContext(cx string) *Error {
	var msg string
	switch *k {
	case DuplicateRequestID:
		msg = fmt.Sprintf("Id (%s) is already being used by another query.", cx)
	case Query:
		msg = fmt.Sprintf("Failed to execute query: %s", cx)
	case InvalidSyntax:
		msg = fmt.Sprintf("Syntax not supported: %s", cx)
	default:
		msg = cx
	}

	return &Error{
		Kind:    *k,
		Message: msg,
	}
}

type Error struct {
	Kind    ErrorKind
	Message string
}

func (e *Error) Error() string {
	return fmt.Sprintf("Error %d: %s", e.Kind, e.Message)
}
