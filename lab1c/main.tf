# 1. Configuracion del Proveedor
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# 2. Grupo de Recursos para DESARROLLO
resource "azurerm_resource_group" "dev" {
  name     = "rg-lab1btf-dev"
  location = "North Europe"

  tags = {
    Workload = "lab1b"
    Owner    = "tu-email@institucion.com"
  }
}

# 3. Grupo de Recursos para PRODUCCION
resource "azurerm_resource_group" "prod" {
  name     = "rg-lab1btf-prod"
  location = "North Europe"

  tags = {
    Workload = "lab1b"
    Owner    = "tu-email@institucion.com"
  }
}
