import { router } from "expo-router";
import { Pressable, Text, TextInput, View } from 'react-native';
import { useSession } from "@/context/auth-ctx";
import { useForm, Controller } from 'react-hook-form';

export type LoginFormData = {
    email: string;
    password: string;
}


export default function LoginScreen() {
    const { login } = useSession();

    const {
        control,
        handleSubmit,
        formState: { isSubmitting },
    } = useForm<LoginFormData>({
        defaultValues: {
            email: '',
            password: ''
        }
    })

    const onSubmit = async (data: LoginFormData) => {
        login(data)
        router.replace('/')
    }

    return (
        <View className="flex-1 justify-center m-auto">
            <Text className="text-rose">Email</Text>
            <Controller
                control={control}
                name="email"
                rules={{
                    required: 'Email is required',
                    pattern: {
                        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                        message: 'Invalid email address'
                    },
                }}
                render={({ field: { onChange, onBlur, value} }) => (
                    <TextInput
                        style={''}
                        onBlur={onBlur}
                        onChangeText={onChange}
                        value={value}
                        keyboardType="email-address"
                        autoCapitalize="none"
                        placeholder="Enter you email"
                    />
                )}
            />

            <Text>Password</Text>
            <Controller
                control={control}
                name="password"
                rules={{
                    required: 'Password is required',
                }}
                render={({ field: { onChange, onBlur, value } }) => (
                    <TextInput
                        style={''}
                        onBlur={onBlur}
                        onChangeText={onChange}
                        value={value}
                        secureTextEntry
                        placeholder="Enter your password"
                    />
                )}
            />

            <Pressable
                onPress={handleSubmit(onSubmit)}
                disabled={isSubmitting}
            >
                <Text>{isSubmitting ? 'Logging In...': 'Login' }</Text>
            </Pressable>
        </View>
    )
}