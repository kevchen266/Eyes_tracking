package com.example.eyetracking.model;

public class CalibrationUser {
    private String userId;
    private String images;
    private int age;
    private int gender;
    private int[] coordinates;

    public CalibrationUser(String userId,String images,int age,int gender,int[] coordinates){
        this.userId=userId;
        this.images=images;
        this.age=age;
        this.gender=gender;
        this.coordinates=coordinates;
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

    public int[] getCoordinates() {
        return coordinates;
    }

    public void setCoordinates(int[] coordinates) {
        this.coordinates = coordinates;
    }
}
