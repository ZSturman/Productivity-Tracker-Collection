//
//  InputExecutionTests.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/24/23.
//

import SwiftUI

struct InputExecutionTests: View {
    
    @State private var showSheet: Bool = false
    
    @State var stackPath: [String] = ["Item Øne", "Item Two"]
    
    var body: some View {
        VStack {
            Button("Add Items") {
                stackPath.append(contentsOf: [
                "Item 5", "Item 4", "Item 3"
                ])
                showSheet.toggle()
            }
            
            Button("Add Stuff") {
                stackPath.append(contentsOf: [
                "Stuff 5", "Stuff 4", "Stuff 3"
                ])
                showSheet.toggle()
            }
        }
        .sheet(isPresented: $showSheet, content: {
            TestScreen(stackPath: $stackPath)
        })
//        .sheet(item: $inputExecution) { model in
//            TestScreen(currentInputExecution: model)
//        }
        

    }
}

#Preview {
    InputExecutionTests()
}


struct RandomModel: Identifiable {
    let id = UUID().uuidString
    let title: String
}

struct TestScreen: View {
    
    @Binding var stackPath: [String]
    
    var body: some View {
        NavigationStack(path: $stackPath) {
            ScrollView {
                VStack {
                    Button("NEXT") {
                        print("Next pressed on sheet")
                    }
                    
                }
            }
            .navigationTitle("Items and Stuffs")
            .navigationDestination(for: String.self) { value in
                    Text("ANOTHER SCREEN: \(value)")
            }
        }
    }
}

