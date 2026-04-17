param name string = 'swa-psi-solution-architecture'
param location string = 'westeurope'
param sku string = 'Free'

resource staticWebApp 'Microsoft.Web/staticSites@2022-09-01' = {
  name: name
  location: location
  sku: {
    name: sku
    tier: sku
  }
  properties: {}
}

output defaultHostname string = staticWebApp.properties.defaultHostname
output id string = staticWebApp.id
