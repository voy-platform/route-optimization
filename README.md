### POST request to https://route-optimization-pearl.vercel.app/api/optimize-route

example body:

```json
{
  "dc": {
    "id": "DC101",
    "name": "Charlottesville Central",
    "coordinates": [
      38.0293,
      -78.4767
    ]
  },
  "stops": [
    {
      "id": "1de9ea66-70d3-4a1f-8735-df5ef7697fb9",
      "coordinates": [
        37.982591,
        -78.445604
      ]
    },
    {
      "id": "87b8a518-e065-43eb-b411-3cb033354fc7",
      "coordinates": [
        38.045872,
        -78.483076
      ]
    },
    {
      "id": "7888fa7a-eed6-4a5a-886b-7f7f0b9ab366",
      "coordinates": [
        37.973178,
        -78.410776
      ]
    },
    {
      "id": "b30b0b98-f060-4517-aecd-a947caf4a2a1",
      "coordinates": [
        37.955487,
        -78.451799
      ]
    },
    {
      "id": "8bcae492-d7a3-44ea-a51a-0926ece37d77",
      "coordinates": [
        37.999205,
        -78.409798
      ]
    },
    {
      "id": "2a527521-7d91-4f7b-86e2-11a03b84edf7",
      "coordinates": [
        38.041806,
        -78.474868
      ]
    },
    {
      "id": "88b66e13-128e-48f7-876e-d0d1bfe389a3",
      "coordinates": [
        38.029183,
        -78.38869
      ]
    },
    {
      "id": "e0bac506-23d3-457c-bde1-32a9f33f2c41",
      "coordinates": [
        38.003582,
        -78.54189
      ]
    },
    {
      "id": "c67c2e9a-3657-4fb3-848f-1b2ca3b152d3",
      "coordinates": [
        37.977106,
        -78.487953
      ]
    },
    {
      "id": "2c9b6d3d-ba18-4596-9e21-ba89d57ed9be",
      "coordinates": [
        37.963831,
        -78.522401
      ]
    },
    {
      "id": "0785930b-43bb-49f9-b318-a7b7ed711826",
      "coordinates": [
        37.981232,
        -78.461811
      ]
    },
    {
      "id": "49449c40-d53d-4f90-bf68-ae6950ad4b42",
      "coordinates": [
        38.049517,
        -78.523295
      ]
    },
    {
      "id": "6e534c59-f303-4664-87b6-8cc2eab87eb7",
      "coordinates": [
        38.08071,
        -78.422363
      ]
    },
    {
      "id": "7c1dc4f8-9049-4277-b84e-a1bec7c73f30",
      "coordinates": [
        38.118678,
        -78.570616
      ]
    },
    {
      "id": "2ebe0b6a-e211-4911-89d0-e84dc111696b",
      "coordinates": [
        37.961787,
        -78.447346
      ]
    },
    {
      "id": "181338b2-de91-4c34-896d-5e469ea1a1b9",
      "coordinates": [
        37.942047,
        -78.456156
      ]
    }
  ],
  "num_of_vehicles": 15,
  "max_stops_per_vehicle": 6
}
```
