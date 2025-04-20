import React, { useState } from 'react';
import { Form, Button, Container, Header, Segment, Grid, Message, Loader } from 'semantic-ui-react';
import { WorkApi } from '../misc/WorkApi';
import { handleLogError } from '../misc/Helpers';
import { motion } from 'framer-motion';

const FEATURE_NAMES = [
    ['mean_radius', 'Mean Radius'], 
    ['mean_texture', 'Mean Texture'], 
    ['mean_perimeter', 'Mean Perimeter'],
    ['mean_area', 'Mean Area'], 
    ['mean_smoothness', 'Mean Smoothness'], 
    ['mean_compactness', 'Mean Compactness'],
    ['mean_concavity', 'Mean Concavity'], 
    ['mean_concave_points', 'Mean Concave Points'], 
    ['mean_symmetry', 'Mean Symmetry'],
    ['mean_fractal_dimension', 'Mean Fractal Dimension'], 
    ['radius_error', 'Radius Error'], 
    ['texture_error', 'Texture Error'],
    ['perimeter_error', 'Perimeter Error'], 
    ['area_error', 'Area Error'], 
    ['smoothness_error', 'Smoothness Error'],
    ['compactness_error', 'Compactness Error'], 
    ['concavity_error', 'Concavity Error'], 
    ['concave_points_error', 'Concave Points Error'],
    ['symmetry_error', 'Symmetry Error'], 
    ['fractal_dimension_error', 'Fractal Dimension Error'], 
    ['worst_radius', 'Worst Radius'],
    ['worst_texture', 'Worst Texture'], 
    ['worst_perimeter', 'Worst Perimeter'], 
    ['worst_area', 'Worst Area'],
    ['worst_smoothness', 'Worst Smoothness'], 
    ['worst_compactness', 'Worst Compactness'], 
    ['worst_concavity', 'Worst Concavity'],
    ['worst_concave_points', 'Worst Concave Points'], 
    ['worst_symmetry', 'Worst Symmetry'], 
    ['worst_fractal_dimension', 'Worst Fractal Dimension']
];

const PredictionForm = () => {
    const [formData, setFormData] = useState({});
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setIsLoading(true);
        try {
            const response = await WorkApi.predict(formData);
            setResult(response.data.result);
        } catch (error) {
            handleLogError(error);
            setError('Failed to connect to server. Please ensure the backend is running.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleRefresh = () => {
        setFormData({});
        setResult(null);
        setError(null);
        setIsLoading(false);
        // Clear all form inputs
        const inputs = document.querySelectorAll('input[type="number"]');
        inputs.forEach(input => input.value = '');
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <Container style={{ marginTop: '2em' }}>
                <Segment padded='very' raised className="glass-morphism">
                    <motion.div
                        initial={{ scale: 0.9 }}
                        animate={{ scale: 1 }}
                        transition={{ duration: 0.3 }}
                    >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2em' }}>
                            <Header as='h2' color='purple'>
                                Breast Cancer Prediction
                            </Header>
                            <motion.div
                                whileHover={{ scale: 1.1 }}
                                whileTap={{ scale: 0.9 }}
                            >
                                <Button 
                                    icon='refresh'
                                    color='purple'
                                    onClick={handleRefresh}
                                    circular
                                    size='large'
                                    className="hover-effect"
                                />
                            </motion.div>
                        </div>
                        <Form onSubmit={handleSubmit} className="animated-form">
                            <Grid columns={2} stackable>
                                {FEATURE_NAMES.map(([fieldName, label], index) => (
                                    <Grid.Column key={fieldName}>
                                        <motion.div
                                            initial={{ opacity: 0, x: -20 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            transition={{ delay: index * 0.05 }}
                                        >
                                            <Form.Field className="form-field-animation">
                                                <label>{label}</label>
                                                <Form.Input
                                                    type="number"
                                                    step="any"
                                                    required
                                                    className="input-animation"
                                                    onChange={(e) => setFormData({
                                                        ...formData,
                                                        [fieldName]: parseFloat(e.target.value)
                                                    })}
                                                />
                                            </Form.Field>
                                        </motion.div>
                                    </Grid.Column>
                                ))}
                            </Grid>
                            <motion.div 
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                style={{ textAlign: 'center', marginTop: '2em' }}
                            >
                                <Button type='submit' color='purple' size='large'>
                                    Predict
                                </Button>
                            </motion.div>
                        </Form>
                        {error && (
                            <Message negative>
                                <Message.Header>Error</Message.Header>
                                <p>{error}</p>
                            </Message>
                        )}
                        {isLoading && (
                            <div style={{ textAlign: 'center', marginTop: '1em' }}>
                                <Loader active inline='centered' />
                            </div>
                        )}
                        {result && (
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.5 }}
                            >
                                <Message
                                    style={{ marginTop: '1em' }}
                                    positive={!result.includes('Cancer')}
                                    negative={result.includes('Cancer')}
                                >
                                    <Message.Header>{result}</Message.Header>
                                </Message>
                            </motion.div>
                        )}
                    </motion.div>
                </Segment>
            </Container>
        </motion.div>
    );
};

export default PredictionForm;
