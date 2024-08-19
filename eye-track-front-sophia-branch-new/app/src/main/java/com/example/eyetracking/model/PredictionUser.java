package com.example.eyetracking.model;

public class PredictionUser {
    private String userId;
    private String images;
    private int age;
    private int gender;

    public PredictionUser(String userId,String images,int age,int gender){
        this.userId=userId;
        this.images=images;
        this.age=age;
        this.gender=gender;
    }

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getImages() {
        return images;
    }

    public void setImages(String images) {
        this.images = images;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public int getGender() {
        return gender;
    }

    public void setGender(int gender) {
        this.gender = gender;
    }
}
