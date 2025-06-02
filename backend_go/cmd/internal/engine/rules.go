// backend_go/internal/engine/rules.go
package engine

import (
	"strings"

	"ayaan/internal/models"
)

func EvaluateRules(txn models.Transaction) bool {
	// Example basic fraud rules
	if txn.Amount > 10000 {
		return true // flag large transactions
	}
	if strings.Contains(strings.ToLower(txn.Location), "unknown") {
		return true // suspicious location
	}
	return false
}
