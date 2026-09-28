import { useState } from 'react'

function Formulario({ onAgregar }) {
  const [nombre, setNombre] = useState('')
  const [categoria, setCategoria] = useState('')
  const [tecnologia, setTecnologia] = useState('')

  function manejarEnvio(event) {
    event.preventDefault()

    if (!nombre || !categoria || !tecnologia) {
        alert('Completa todos los campos')
        return
    }

    onAgregar({
      nombre: nombre,
      categoria: categoria,
      tecnologia: tecnologia
    })

    setNombre('')
    setCategoria('')
    setTecnologia('')
  }

  return (
    <form onSubmit={manejarEnvio}>
      <h2>Registrar tecnología</h2>

      <label>
        Nombre:
        <input
          type="text"
          value={nombre}
          onChange={(event) => setNombre(event.target.value)}
        />
      </label>

      <br />

      <label>
        Categoría:
        <input
          type="text"
          value={categoria}
          onChange={(event) => setCategoria(event.target.value)}
        />
      </label>

      <br />

      <label>
        Tecnología:
        <input
          type="text"
          value={tecnologia}
          onChange={(event) => setTecnologia(event.target.value)}
        />
      </label>

      <br />

      <button type="submit">
        Registrar
      </button>
    </form>
  )
}

export default Formulario