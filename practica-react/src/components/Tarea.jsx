function Tarea({ id, nombre, descripcion, estado, onCambiarEstado, onEliminar }) {
  return (
    <article>
      <h2>{nombre}</h2>

      <p>{descripcion}</p>

      <p>
        Estado: <strong>{estado}</strong>
      </p>

      <button onClick={() => onCambiarEstado(id)}>
        Cambiar estado
      </button>

      <button onClick={() => onEliminar(id)}>
        Eliminar
      </button>
    </article>
  )
}

export default Tarea