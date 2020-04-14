"""
Created on Fri Sep  6 08:26:09 2019

@author: rahulsurasinghe 

Summary: Used to validate app spec files
"""
import yaml
from jsonschema import validate 

# Where the app spec is located on Jenkins node 
path = 'apprepo/values.yaml' 

# Checks incoming app spec to correct shema in order to validate it
schema = '''
type: object 
properties: 
  replicaCount: 
    type: integer 
    description: How many pods you want deployed  
  name: 
    type: string 
    description: Name of the deployment 
  image: 
    type: object 
    properties: 
      repository: 
        type: string 
        description: Name of the artifactory repo the image is being pulled from 
      tag: 
        type: [string, number] 
        description: The version of the image 
      pullPolicy: 
        type: string 
        enum: [IfNotPresent, Always, None]
        description: How to pull the image 
    required: [repository, tag, pullPolicy] 

  nameOverride: 
    type: string 
  fullnameOverride: 
    type: string   

  service: 
    type: object
    properties:  
      type: 
        type: string  
        enum: [ClusterIP, NodePort, LoadBalancer, ExternalName]
        description: Type of service
      port: 
        type: integer 
        description: Port in which the service is listening in on  
    required: [type, port] 
    
  ingress:
    type: object 
    properties:  
      enabled: 
        type: boolean 
        description: Have Helm create ingress for you or not 
      annotations: 
        type: object 
      labels: 
        type: object  
      hosts: 
        type: array 
        items: [type: string]
        uniqueItems: true 
      tls: 
        properties: 
          secretName: 
            type: string 
          hosts: 
            type: array 
            items: [type: string] 
            uniqueItems: true 
        required: [secretName, hosts]
      hosts: 
        properties: 
          host: 
            type: array
            items: [type: string]
            uniqueItems: true 
          paths: 
            type: array 
        required: [host, paths] 
    required: [enabled] 

  resources: 
    type: object  
    description: Resource limits and requests of the app.
    properties: 
      limits: 
        type: object 
        properties: 
          cpu: 
            type: [number, string] 
          memory: 
            type: [number, string]  
      requests: 
        type: object 
        properties: 
          cpu: 
            type: [number, string] 
          memory: 
            type: [number, string]
    required: [limits, requests]

  nodeSelctor: 
    type: object
  tolerations: 
    type: array 
  affinity: 
    type: object   

required: [replicaCount, name, image, service, ingress, resources]         
'''

print(validate(yaml.safe_load(path), yaml.safe_load(schema)))