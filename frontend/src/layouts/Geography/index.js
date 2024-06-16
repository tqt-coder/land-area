import { Button, Col, Form, Row, Select } from 'antd';
import { useEffect, useState } from 'react';
import { Controller, useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import LocationService from '../../services/location';
import './styles.css';

const Geography = () => {
    const [provinces, setProvinces] = useState([]);
    const [cities, setCities] = useState([]);
    const [wards, setWards] = useState([]);
    const [responseText, setResponseText] = useState('');
    const navigate = useNavigate();
    const { control, setValue, watch, handleSubmit } = useForm({
        defaultValues: {
            province: null,
            city: null,
            ward: null,
            url_label: '',
            url_mask: '',
            url_fordel_img: '',
        },
    });

    const getProvinces = async () => {
        try {
            const provinces = await LocationService.getProvincesOrCities(navigate);
            setProvinces(provinces);
        } catch (error) {
            alert(error.message);
        }
    };

    const getCities = async (provinceId) => {
        try {
            const cities = await LocationService.getDistrictsOrCities(provinceId, navigate);
            setCities(cities);
        } catch (error) {
            alert(error.message);
        }
    };

    const getWards = async (cityId) => {
        try {
            const wards = await LocationService.getWardsOrCommunes(cityId, navigate);
            setWards(wards);
        } catch (error) {
            alert(error.message);
        }
    };

    const handleFieldChange = (field, value) => {
        switch (field) {
            case 'province': {
                setValue('city', null);
                setValue('ward', null);
                setValue('province', value);
                getCities(value);
                break;
            }
            case 'city': {
                setValue('ward', null);
                setValue('city', value);
                getWards(value);
                break;
            }
            case 'ward': {
                setValue('ward', value);
                break;
            }
            default: {
                break;
            }
        }
    };

    useEffect(() => {
        getProvinces();
    }, []);

    const handleInspectRegion = async () => {
        const { url_label, url_mask } = watch();
        if (!url_label || !url_mask) {
            alert('Please provide both URL label and URL mask.');
            return;
        }
        const { province, city, ward } = watch(); // Get form data
        if (!province || !city || !ward) {
            alert('Please select province, city, and ward.');
            return;
        }
        try {
            const selectedWard = wards.find((item) => item.code === ward);
            if (!selectedWard) {
                alert('Selected ward not found.');
                return;
            }
            const queryParams = new URLSearchParams();
            queryParams.set('ward', encodeURIComponent(selectedWard.full_name));
            queryParams.set('url_label', encodeURIComponent(url_label));
            queryParams.set('url_mask', encodeURIComponent(url_mask));
            
            // Navigate to dashboard with encoded parameters
            navigate(`/admin/dashboard?${queryParams.toString()}`);
        } catch (error) {
            setResponseText(error.message);
        }
    };

    const handleDownloadImage = async (data) => {
        const { province, city, ward } = data;
        if (!province || !city || !ward) {
            alert('Please select province, city, and ward.');
            return;
        }
        try {
            const selectedWard = wards.find((item) => item.code === ward);
            const selectedDistrict = cities.find((item) => item.code === city);
            const selectedCity = provinces.find((item) => item.code === province);
            const response = await LocationService.downloadImage(selectedCity.name, selectedDistrict.name, selectedWard.name);

            if (response.status === 200 && response.message) {
                setResponseText(response.message);
            } else {
                setResponseText('Unexpected response format');
            }
        } catch (error) {
            alert(error)
            setResponseText(error);
        }
    };

    const handleInference = async (data) => {
        const { url_mask, url_fordel_img } = data;
        if (!url_mask || !url_fordel_img) {
            alert('Please provide both URL mask and URL folder image.');
            return;
        }
        try {
            const response = await LocationService.inferenceImage(url_mask, url_fordel_img);
            if (response.status === 200 &&  response.message) {
                setResponseText(response.message);
            } else {
                setResponseText('Unexpected response format');
            }
        } catch (error) {
            setResponseText(error.message);
        }
    };

    const onSubmit = (data) => {
        handleDownloadImage(data);
    };

    return (
        <div className='content'>
            <h1>Find Regional Planning</h1>
            <hr style={{ backgroundColor: '#fff' }} />
            <Form layout='vertical' onFinish={handleSubmit(onSubmit)}>
                <Row gutter={16} style={{ marginBottom: '25px' }}>
                    <Col span={7}>
                        <Form.Item label='Province/City'>
                            <Controller
                                name='province'
                                control={control}
                                rules={{ required: true }}
                                render={({ field }) => (
                                    <Select
                                        {...field}
                                        allowClear
                                        showSearch
                                        size='large'
                                        placeholder='Select a province/city'
                                        onChange={(value) => handleFieldChange('province', value)}
                                        optionFilterProp='children'
                                        filterOption={(input, option) => {
                                            return option.children
                                                .toLowerCase()
                                                .includes(input.toLowerCase());
                                        }}
                                    >
                                        {provinces.map((province) => (
                                            <Select.Option
                                                key={province.code}
                                                value={province.code}
                                            >
                                                {province.full_name}
                                            </Select.Option>
                                        ))}
                                    </Select>
                                )}
                            />
                        </Form.Item>
                    </Col>
                    <Col span={7}>
                        <Form.Item label='City/District'>
                            <Controller
                                name='city'
                                control={control}
                                rules={{ required: true }}
                                render={({ field }) => (
                                    <Select
                                        {...field}
                                        allowClear
                                        size='large'
                                        showSearch
                                        placeholder='Select a city/district'
                                        onChange={(value) => handleFieldChange('city', value)}
                                        optionFilterProp='children'
                                        filterOption={(input, option) => {
                                            return option.children
                                                .toLowerCase()
                                                .includes(input.toLowerCase());
                                        }}
                                    >
                                        {cities.map((city) => (
                                            <Select.Option key={city.code} value={city.code}>
                                                {city.full_name}
                                            </Select.Option>
                                        ))}
                                    </Select>
                                )}
                            />
                        </Form.Item>
                    </Col>
                    <Col span={7}>
                        <Form.Item label='Ward/Commune'>
                            <Controller
                                name='ward'
                                control={control}
                                rules={{ required: true }}
                                render={({ field }) => (
                                    <Select
                                        {...field}
                                        allowClear
                                        showSearch
                                        size='large'
                                        placeholder='Select a ward/commune'
                                        onChange={(value) => handleFieldChange('ward', value)}
                                        optionFilterProp='children'
                                        filterOption={(input, option) => {
                                            return option.children
                                                .toLowerCase()
                                                .includes(input.toLowerCase());
                                        }}
                                    >
                                        {wards.map((ward) => (
                                            <Select.Option key={ward.code} value={ward.code}>
                                                {ward.full_name}
                                            </Select.Option>
                                        ))}
                                    </Select>
                                )}
                            />
                        </Form.Item>
                    </Col>
                </Row>
                <Row gutter={16} style={{ marginBottom: '100px' }}>
                    <Col span={8}>
                        <Form.Item className='btn-submit'>
                            <Button type='primary' size='large' htmlType='submit'>
                                Download Image
                            </Button>
                        </Form.Item>
                    </Col>
                    <Col span={8}>
                        <Form.Item className='btn-submit'>
                            <Button type='primary2' onClick={() => handleInference(watch())} className='btn-yellow' size='large'>
                                Inference Image
                            </Button>
                        </Form.Item>
                    </Col>
                    <Col span={8}>
                        <Form.Item className='btn-submit'>
                            <Button
                                type='primary3'
                                className='btn-green'
                                size='large'
                                onClick={handleInspectRegion}
                            >
                                Inspect Region
                            </Button>
                        </Form.Item>
                    </Col>
                </Row>
                    <Row gutter={16}>
                        <Col span={7}>
                            <Form.Item label='Link folder label'>
                                <Controller
                                    name='url_label'
                                    control={control}
                                    render={({ field }) => <input {...field} />}
                                />
                            </Form.Item>
                        </Col>
                        <Col span={7}>
                            <Form.Item label='Link folder mask'>
                                <Controller
                                    name='url_mask'
                                    control={control}
                                    render={({ field }) => <input {...field} />}
                                />
                            </Form.Item>
                        </Col>
                        <Col span={7}>
                            <Form.Item label='Link folder image'>
                                <Controller
                                    name='url_fordel_img'
                                    control={control}
                                    render={({ field }) => <input {...field} />}
                                />
                            </Form.Item>
                        </Col>
                    </Row>
                {responseText && (
                    <Row gutter={16}>
                        <Col span={24}>
                            <hr style={{ backgroundColor: '#fff' }} />
                            <div className='response-text'>
                                <h2 style={{ fontSize: '20px', textAlign: 'center', marginTop: '50px' }}>Link: {responseText}</h2>
                            </div>
                        </Col>
                    </Row>
                )}
            </Form>
        </div>
    );
};

export default Geography;
