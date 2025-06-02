// backend_go/internal/api/handler.go
package api

import (
	"encoding/json"
	"log"
	"net/http"

	"ayaan/internal/engine"
	"ayaan/internal/models"
)

func HandleIngest(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var txn models.Transaction
	err := json.NewDecoder(r.Body).Decode(&txn)
	if err != nil {
		http.Error(w, "Invalid payload", http.StatusBadRequest)
		return
	}

	flagged := engine.EvaluateRules(txn)
	response := map[string]interface{}{
		"flagged": flagged,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
	log.Printf("[Transaction] %+v | Flagged: %v", txn, flagged)
}
