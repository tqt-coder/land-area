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
    const navigate = useNavigate();
    const { control, handleSubmit, setValue } = useForm({
        defaultValues: {
            province: null,
            city: null,
            ward: null,
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

    const onSubmit = (data) => {
        const selectedWard = wards.find(ward => ward.code === data.ward);
        navigate(`/admin/dashboard?ward=${selectedWard.full_name}&wardCode=${selectedWard.code}`);
    };

    return (
        <div className='content'>
            <h1>Find Regional Planning</h1>
            <hr style={{ backgroundColor: '#fff' }} />
            <Form layout='vertical' onFinish={handleSubmit(onSubmit)}>
                <Row gutter={16}>
                    <Col span={6}>
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
                    <Col span={6}>
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
                    <Col span={6}>
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
                    <Col span={6}>
                        <Form.Item className='btn-submit'>
                            <Button type='primary' size='large' htmlType='submit'>
                                Inspect Region
                            </Button>
                        </Form.Item>
                    </Col>
                </Row>
            </Form>
        </div>
    );
};

export default Geography;
