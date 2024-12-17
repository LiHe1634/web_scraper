import React from 'react';
import { Modal, Form, Input, Select, message } from 'antd';
import { taskAPI } from '../../services/api';

const { Option } = Select;

const TaskForm = ({ visible, onCancel, onSuccess, initialValues }) => {
  const [form] = Form.useForm();

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      if (initialValues?.id) {
        await taskAPI.updateTask(initialValues.id, values);
        message.success('任务更新成功');
      } else {
        await taskAPI.createTask(values);
        message.success('任务创建成功');
      }
      form.resetFields();
      onSuccess();
    } catch (error) {
      message.error('提交失败: ' + error.message);
    }
  };

  return (
    <Modal
      title={initialValues ? '编辑任务' : '新建任务'}
      open={visible}
      onCancel={onCancel}
      onOk={handleSubmit}
      destroyOnClose
    >
      <Form
        form={form}
        layout="vertical"
        initialValues={initialValues}
      >
        <Form.Item
          name="name"
          label="任务名称"
          rules={[{ required: true, message: '请输入任务名称' }]}
        >
          <Input placeholder="请输入任务名称" />
        </Form.Item>

        <Form.Item
          name="url"
          label="目标URL"
          rules={[
            { required: true, message: '请输入目标URL' },
            { type: 'url', message: '请输入有效的URL' }
          ]}
        >
          <Input placeholder="请输入目标URL" />
        </Form.Item>

        <Form.Item
          name="schedule"
          label="执行计划"
          tooltip="Cron表达式，例如: */5 * * * * 表示每5分钟执行一次"
        >
          <Input placeholder="请输入Cron表达式" />
        </Form.Item>

        <Form.Item
          name="priority"
          label="优先级"
          initialValue="MEDIUM"
        >
          <Select>
            <Option value="LOW">低</Option>
            <Option value="MEDIUM">中</Option>
            <Option value="HIGH">高</Option>
          </Select>
        </Form.Item>

        <Form.Item
          name="config"
          label="配置信息"
          tooltip="JSON格式的配置信息"
        >
          <Input.TextArea
            placeholder="请输入JSON格式的配置信息"
            rows={4}
          />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default TaskForm;
