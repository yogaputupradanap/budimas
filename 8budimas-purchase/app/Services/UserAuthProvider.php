<?php

namespace App\Services;

use App\Models\User;
use Illuminate\Contracts\Auth\Authenticatable;
use Illuminate\Contracts\Auth\UserProvider;

class UserAuthProvider implements UserProvider
{
    /**
     * Retrieve a User by The Given Credentials.
     *
     * @param array $credentials
     * @return \Illuminate\Contracts\Auth\Authenticatable|null
     */
    public function retrieveByCredentials(array $credentials)
    {
        if (empty($credentials)) {
            return;
        }
        return (new User)->fetchUserByCredentials($credentials);
    }

    /**
     * Validate a User Against the Given Credentials.
     *
     * @param \Illuminate\Contracts\Auth\Authenticatable $user
     * @param array $credentials
     * @return bool
     */
    public function validateCredentials(Authenticatable $auth, array $credentials)
    {
        return (
            $credentials['username'] == $auth->getAuthUsername()
        );
    }

    /**
     * Retrieve a User Data by Saved Identifier Session.
     *
     * @param array $identifier
     * @return \App\Models\User
     */
    public function find($identifier)
    {
        $tokens = (new User)
            ->select('/api/extra/getUserToken', 'GET', ['id' => $identifier])
            ->first()
            ->tokens;
        return (new User)
            ->token($tokens)
            ->where(['users.id', '=', $identifier])
            ->select('/api/extra/getUser');
    }

    /**
     * Retrieve a User by Their Unique Identifier and Token.
     * This is Not be Used, But Need to be Declared
     * in order to Implementing the UserProvider Class.
     *
     * @param  mixed  $identifier
     * @param  string  $token
     * @return \Illuminate\Contracts\Auth\Authenticatable|null
     */
    public function retrieveByToken($identifier, $token)
    {
        return (new User)
            ->token($auth->getRememberToken())
            ->where([$auth->getAuthIdentifierName(), '=', $auth->getAuthIdentifier()])
            ->where([$auth->getRememberTokenName(), '=', $auth->getRememberToken()])
            ->select();
    }

    /**
     * Update the Token for the Given User in Storage.
     * This is Not be Used, But Need to be Declared
     * in order to Implementing the UserProvider Class.
     *
     * @param  \Illuminate\Contracts\Auth\Authenticatable $user
     * @param  string  $token
     * @return void
     */
    public function updateRememberToken(Authenticatable $auth, $token)
    {
        (new User)
            ->token($auth->getRememberToken())
            ->where([$auth->getAuthIdentifierName(), '=', $auth->getAuthIdentifier()])
            ->update([$auth->getRememberTokenName() => $token]);
    }
}
