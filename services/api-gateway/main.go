package main

import (
	"net/http"
	"net/http/httputil"
	"net/url"
	"time"

	"github.com/gin-contrib/cors" // Importa o novo pacote de CORS
	"github.com/gin-gonic/gin"
)

// reverseProxy cria um manipulador de proxy para um serviço de destino.
func reverseProxy(target string) gin.HandlerFunc {
	url, err := url.Parse(target)
	if err != nil {
		panic(err)
	}
	proxy := httputil.NewSingleHostReverseProxy(url)
	return func(c *gin.Context) {
		proxy.ServeHTTP(c.Writer, c.Request)
	}
}

func main() {
	router := gin.Default()

	// --- Configuração do CORS ---
	// Define qual origem (nosso frontend) tem permissão para fazer requisições.
	config := cors.Config{
		AllowOrigins:     []string{"http://localhost:3000", "http://localhost:5000"}, // Permite as portas comuns do frontend
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}
	router.Use(cors.New(config))

	// Define os serviços de backend.
	userService := reverseProxy("http://usuarios-service:8000")
	agendamentoService := reverseProxy("http://srv-agendamentos:8000")

	// --- Roteamento para os Microsserviços ---
	v1 := router.Group("/api/v1")
	{
		v1.Any("/auth/*proxyPath", userService)
		v1.Any("/pacientes/*proxyPath", userService)
		v1.Any("/medicos/*proxyPath", userService)
		v1.Any("/usuarios/*proxyPath", userService)
		v1.Any("/agendas/*proxyPath", agendamentoService)
		v1.Any("/agendamentos/*proxyPath", agendamentoService)
	}

	router.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"serviço": "API Gateway Zello",
			"status":  "operacional",
		})
	})

	router.Run(":8080")
}