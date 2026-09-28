function Card({ id, nombre, descripcion, categoria, tecnologia, onEliminar }) {
  return (
    <article>
      <h2>{nombre}</h2>
      <p>{descripcion}</p>
      <p>Categoría: {categoria}</p>

      {tecnologia && <p>Tecnología: {tecnologia}</p>}
      
      <button onClick={() => onEliminar(id)}>
        Eliminar
      </button>
    </article>
  )
}

export default Card