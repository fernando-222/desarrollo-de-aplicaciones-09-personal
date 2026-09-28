import { useState } from 'react'
import reactLogo from './assets/react.svg'
import Header from './components/Header'
import Card from './components/Card'
import Footer from './components/Footer'
import Formulario from './components/Formulario'
import Usuarios from './components/Usuarios'
import './App.css'
import Tarea from './components/Tarea'
function App() {
  const [tecnologias, setTecnologias] = useState([
    {
      id: 1,
      nombre: 'React',
      descripcion: 'Biblioteca para construir interfaces de usuario.',
      categoria: 'Frontend'
    },
    {
      id: 2,
      nombre: 'Vite',
      descripcion: 'Herramienta para crear proyectos web modernos.',
      categoria: 'Desarrollo web'
    },
    {
      id: 3,
      nombre: 'JavaScript',
      descripcion: 'Lenguaje utilizado para desarrollar aplicaciones web.',
      categoria: 'Programación'
    },
    {
      id: 4,
      nombre: 'Node.js',
      descripcion: 'Entorno para ejecutar JavaScript fuera del navegador.',
      categoria: 'Backend'
    },
    {
      id: 5,
      nombre: 'Python',
      descripcion: 'Lenguaje de programación de propósito general.',
      categoria: 'Programación'
    }
  ])
function eliminarTecnologia(id) {
  setTecnologias(
    tecnologias.filter((tecnologia) => tecnologia.id !== id)
  )
}  

function agregarTecnologia(nuevaTecnologia) {
  const nueva = {
    id: Date.now(),
    nombre: nuevaTecnologia.nombre,
    descripcion: 'Tecnología registrada mediante el formulario.',
    categoria: nuevaTecnologia.categoria,
    tecnologia: nuevaTecnologia.tecnologia
  }

  setTecnologias([...tecnologias, nueva])
}

const [tareas, setTareas] = useState([
  {
    id: 1,
    nombre: 'Tarea 1',
    descripcion: 'Revisar los apuntes de React.',
    estado: 'Pendiente'
  },
  {
    id: 2,
    nombre: 'Tarea 2',
    descripcion: 'Practicar componentes y props.',
    estado: 'Pendiente'
  },
  {
    id: 3,
    nombre: 'Tarea 3',
    descripcion: 'Repasar useState y eventos.',
    estado: 'En progreso'
  },
  {
    id: 4,
    nombre: 'Tarea 4',
    descripcion: 'Practicar formularios controlados.',
    estado: 'Pendiente'
  },
  {
    id: 5,
    nombre: 'Tarea 5',
    descripcion: 'Repasar consumo de APIs.',
    estado: 'Completada'
  }
])

function cambiarEstado(id) {
  setTareas(
    tareas.map((tarea) =>
      tarea.id === id
        ? {
            ...tarea,
            estado:
              tarea.estado === 'Pendiente'
                ? 'En progreso'
                : tarea.estado === 'En progreso'
                ? 'Completada'
                : 'Pendiente'
          }
        : tarea
    )
  )
}

function eliminarTarea(id) {
  setTareas(tareas.filter((tarea) => tarea.id !== id))
}

  return (
    <div>
      <Header />

      <h2>Estudiante: Fernando Ortiz</h2>

      <Formulario onAgregar={agregarTecnologia} />
      {tecnologias.map((tecnologia) => (
        <Card
          key={tecnologia.id}
          id={tecnologia.id}
          nombre={tecnologia.nombre}
          descripcion={tecnologia.descripcion}
          categoria={tecnologia.categoria}
          tecnologia={tecnologia.tecnologia}
          onEliminar={eliminarTecnologia}
        />
      ))}
      <Usuarios />

      <h2>Panel de tareas</h2>

      {tareas.map((tarea) => (
        <Tarea
          key={tarea.id}
          id={tarea.id}
          nombre={tarea.nombre}
          descripcion={tarea.descripcion}
          estado={tarea.estado}
          onCambiarEstado={cambiarEstado}
          onEliminar={eliminarTarea}
        />
      ))}
      
      <img
        src={reactLogo}
        alt="Logo de React"
        className="imagen"
      />
      
      <Footer />
    </div>
  )
}

export default App