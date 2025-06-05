use relaciones

db.categorias.insertMany([
    {
        _id: ObjectId('6837c7af16403ec0ef6c4bd2'),
        nombre:'Abarrotes'
    },
    {
        _id: ObjectId('6837c7c916403ec0ef6c4bd3'),
        nombre:'Verduras'
    }
])

db.productos.insertMany([
    {
        nombre:'Leche de Almendras',
        precio:14.2,
        categoriaId:ObjectId('6837c7af16403ec0ef6c4bd2')
    },
    {
        nombre:'Perejil',
        precio:1,
        categoriaId:ObjectId('6837c7c916403ec0ef6c4bd3')
    },
    {
        nombre:'Calabaza',
        fechaVencimiento: new Date('2025-06-02T00:00:00')
    },
])

// Asi podemos visualizar la informacion haciendo un 'join' entre las dos colecciones
db.productos.aggregate([
    {
        $lookup: {
        from: "categorias",
        localField: "categoriaId",
        foreignField: "_id",
        as: "categoria"
        }
    }
])