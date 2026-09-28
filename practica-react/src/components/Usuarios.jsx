import { useEffect, useState } from 'react'

function Usuarios() {
  const [usuarios, setUsuarios] = useState([])
  const [cargando, setCargando] = useState(true)
  const [busqueda, setBusqueda] = useState('')

  useEffect(() => {
    fetch('https://jsonplaceholder.typicode.com/users')
      .then((respuesta) => respuesta.json())
      .then((datos) => {
        setUsuarios(datos)
        setCargando(false)
      })
  }, [])

  const usuariosFiltrados = usuarios.filter((usuario) =>
    usuario.name.toLowerCase().includes(busqueda.toLowerCase())
  )

  if (cargando) {
    return <p>Cargando usuarios...</p>
  }

  return (
    <section>
      <h2>Usuarios obtenidos de la API</h2>

      <input
        type="text"
        placeholder="Buscar usuario por nombre"
        value={busqueda}
        onChange={(event) => setBusqueda(event.target.value)}
      />

      {usuariosFiltrados.length === 0 ? (
        <p>No existen coincidencias.</p>
      ) : (
        usuariosFiltrados.map((usuario) => (
          <div key={usuario.id}>
            <h3>{usuario.name}</h3>

            <p>Email: {usuario.email}</p>

            <p>Ciudad: {usuario.address.city}</p>

            <p>Empresa: {usuario.company.name}</p>
          </div>
        ))
      )}
    </section>
  )
}

export default Usuarios