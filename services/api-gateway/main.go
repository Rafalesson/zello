// main.go
package main

import (
	"net/http"
	"github.com/gin-gonic/gin"
)

func main() {
	// Inicializa o roteador Gin com a configuração padrão.
	router := gin.Default()

	// Define uma rota GET para a raiz do serviço.
	router.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"servico": "API Gateway",
			"status": "operacional",
		})
	})

	// Inicia o servidor na porta 8080.
	router.Run(":8080")
}