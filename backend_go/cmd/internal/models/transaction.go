package models

type Transaction struct {
	CustomerName string  `json:"customer_name"`
	Amount       float64 `json:"amount"`
	Location     string  `json:"location"`
	Timestamp    string  `json:"timestamp"`
}
