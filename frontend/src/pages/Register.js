import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { register } from '../services/api';

function Register() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        confirmPassword: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        // Validaciones
        if (formData.password !== formData.confirmPassword) {
            setError('Las contraseñas no coinciden');
            return;
        }

        if (formData.password.length < 6) {
            setError('La contraseña debe tener al menos 6 caracteres');
            return;
        }

        setLoading(true);

        try {
            await register(formData.username, formData.password);
            alert('Usuario registrado correctamente. Por favor, inicia sesión.');
            navigate('/login');
        } catch (err) {
            setError(err.response?.data?.detail || 'Error al registrar usuario');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={styles.container}>
            <div style={styles.card}>
                <h2 style={styles.title}>Control de Gastos</h2>
                <h3 style={styles.subtitle}>Registro de Usuario</h3>

                <form onSubmit={handleSubmit} style={styles.form}>
                    <div style={styles.formGroup}>
                        <label style={styles.label}>Usuario</label>
                        <input
                            type="text"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            required
                            style={styles.input}
                            autoComplete="username"
                        />
                    </div>

                    <div style={styles.formGroup}>
                        <label style={styles.label}>Contraseña</label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            style={styles.input}
                            autoComplete="new-password"
                        />
                    </div>

                    <div style={styles.formGroup}>
                        <label style={styles.label}>Confirmar Contraseña</label>
                        <input
                            type="password"
                            name="confirmPassword"
                            value={formData.confirmPassword}
                            onChange={handleChange}
                            required
                            style={styles.input}
                            autoComplete="new-password"
                        />
                    </div>

                    {error && <div style={styles.error}>{error}</div>}

                    <button type="submit" disabled={loading} style={styles.button}>
                        {loading ? 'Registrando...' : 'Registrarse'}
                    </button>
                </form>

                <div style={styles.footer}>
                    <p>
                        ¿Ya tienes cuenta? <Link to="/login" style={styles.link}>Inicia sesión</Link>
                    </p>
                </div>
            </div>
        </div>
    );
}

const styles = {
    container: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        backgroundColor: '#f5f5f5'
    },
    card: {
        backgroundColor: 'white',
        padding: '2rem',
        borderRadius: '8px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
        width: '100%',
        maxWidth: '400px'
    },
    title: {
        textAlign: 'center',
        color: '#333',
        marginBottom: '0.5rem'
    },
    subtitle: {
        textAlign: 'center',
        color: '#666',
        marginBottom: '2rem',
        fontWeight: 'normal'
    },
    form: {
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem'
    },
    formGroup: {
        display: 'flex',
        flexDirection: 'column',
        gap: '0.5rem'
    },
    label: {
        fontWeight: '500',
        color: '#333'
    },
    input: {
        padding: '0.75rem',
        border: '1px solid #ddd',
        borderRadius: '4px',
        fontSize: '1rem'
    },
    button: {
        padding: '0.75rem',
        backgroundColor: '#28a745',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        fontSize: '1rem',
        cursor: 'pointer',
        fontWeight: '500',
        marginTop: '1rem'
    },
    error: {
        backgroundColor: '#fee',
        color: '#c33',
        padding: '0.75rem',
        borderRadius: '4px',
        textAlign: 'center'
    },
    footer: {
        marginTop: '1.5rem',
        textAlign: 'center',
        color: '#666'
    },
    link: {
        color: '#007bff',
        textDecoration: 'none',
        fontWeight: '500'
    }
};

export default Register;
