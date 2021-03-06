package handlers

import (
	"fmt"
	"net/http"

	"github.com/labstack/echo"
	"gitlab.globoi.com/supseg/a1-sqli/types"
	"gitlab.globoi.com/supseg/a1-sqli/util"
)

//HealthCheck is de health check function
func HealthCheck(c echo.Context) error {
	return c.String(http.StatusOK, "WORKING!\n")
}

//Login is the login function
func Login(c echo.Context) error {

	loginAttempt := types.LoginAttempt{}
	err := c.Bind(&loginAttempt)
	if err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"result": "error", "details": "Error binding login attempt."})
	}

	validUser, err := util.AuthenticateUser(loginAttempt.User, loginAttempt.Pass)
	if err != nil {
		msgUser := err.Error() + "\n"
		return c.JSON(http.StatusOK, msgUser)
	}

	if validUser {
		msgUser := fmt.Sprintf("Bem vindo(a), %s!\n", loginAttempt.User)
		return c.String(http.StatusOK, msgUser)
	}

	msgUser := fmt.Sprintf("Usuário ou senha errados!\n")
	return c.String(http.StatusOK, msgUser)
}

//Register is the function to register a new user on bd
func Register(c echo.Context) error {

	RegisterAttempt := types.RegisterAttempt{}
	err := c.Bind(&RegisterAttempt)
	if err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"result": "error", "details": "Error binding register attempt."})
	}

	userCreated, err := util.NewUser(RegisterAttempt.User, RegisterAttempt.Pass, RegisterAttempt.PassCheck)
	if err != nil {
		msgUser := err.Error() + "\n"
		return c.JSON(http.StatusOK, msgUser)
	}

	if userCreated {
		msgUser := fmt.Sprintf("Usuario " + RegisterAttempt.User + " criado com sucesso!\n")
		return c.String(http.StatusOK, msgUser)
	}

	msgUser := fmt.Sprintf("De duas uma: usuário já existe ou as senhas estao diferentes!\n")
	return c.String(http.StatusOK, msgUser)
}
